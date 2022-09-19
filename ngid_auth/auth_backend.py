from __future__ import unicode_literals

import jwt
import logging
import re
import requests

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.dispatch import Signal

from .models import AccessToken
from .mixins import OAuthClientMixin
from .provider import get_oauth_provider
import traceback


SESSION_OAUTH_TOKEN_ID = '_auth_user_oauth_token_id'

logger = logging.getLogger('nextgis_common.ngid_auth.backands')


UserModel = get_user_model()


signal_userinfo_got = Signal(providing_args=['user', 'userinfo', 'roles'])


class NgidBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        try:
            nguid = kwargs.get('nguid')
            access_token = kwargs.get('access_token')

            access = AccessToken.objects.filter(user_id=nguid, access_token=access_token).select_related('user')[0]
        except IndexError:
            return None
        else:
            return access.user


class OAuthBaseBackend(OAuthClientMixin, ModelBackend):
    LOGGER_MSG_PREFIX = None

    def introspect(self, access_token):
        oauth_provider = get_oauth_provider()

        introspection_data = requests.post(
            oauth_provider.introspection_url,
            params={'token': access_token},
            auth=requests.auth.HTTPBasicAuth(oauth_provider.consumer_key, oauth_provider.consumer_secret)
        )

        introspection_data = introspection_data.json()

        if introspection_data.get('active'):
            return {
                'access_token': access_token,
                'expires_at': introspection_data['exp']
            }

    def update_or_create_user(self, oauth_token_info):
        userinfo = self.get_userinfo(oauth_token_info)

        if userinfo is None:
            return

        user_guid = self.clean_user_guid(userinfo)

        if user_guid is None:
            return

        defaults = self.clean_user_data(userinfo)

        user, created = UserModel._default_manager.update_or_create(
            nextgis_guid=user_guid,
            defaults=defaults,
        )

        roles = self.try_get_roles(userinfo)
        signal_userinfo_got.send(sender=self.__class__, user=user, userinfo=userinfo, roles=roles)

        return user

    def get_userinfo(self, oauth_token_info):
        userinfo = None

        provider = get_oauth_provider()
        oaut_session = self.get_oauth_session(provider, token=oauth_token_info)
        info_raw_resp = oaut_session.get(provider.profile_url)
        info_raw_resp.raise_for_status()

        userinfo = info_raw_resp.json() or info_raw_resp.text

        return userinfo

    def clean_user_guid(self, userinfo):
        return userinfo.get('user_guid')

    def clean_user_data(self, userinfo):
        return {
            'username': userinfo.get('username'),
            'first_name': userinfo.get('first_name'),
            'last_name': userinfo.get('last_name'),
            'email': userinfo.get('email'),
        }

    def try_get_roles(self, userinfo):
        # It's just for RTI proj, but can be extended
        provider = get_oauth_provider()

        return userinfo.get(
            'resource_access', {}
        ).get(
            provider.consumer_key, {}
        ).get(
            'roles', []
        )

    def make_log_msg(self, msg):
        return '%s. %s' % (self.LOGGER_MSG_PREFIX or self.__class__.__name__, msg)


class OAuthBearerBackend(OAuthBaseBackend):

    def get_bearer_token_from_http_auth(self, http_auth):
        match = re.match(r'Bearer (.*)', http_auth)

        if match is None:
            return None

        return match.groups()[0]

    def authenticate(self, request):
        http_auth = request.META.get("HTTP_AUTHORIZATION")

        if http_auth is None:
            return

        http_access_token = self.get_bearer_token_from_http_auth(http_auth)

        if http_access_token is None:
            return

        # logger.debug(self.make_log_msg('Token: %s' % http_access_token))

        access = AccessToken.objects.find(http_access_token)


        is_good_token = True
        is_expired = False
        str_token_search = 'token was not found :( '
        if access:
            str_token_search = f'token was found! id: {access.id} '
            if access.is_expired:
                is_good_token = False
                is_expired = True
        else:
            is_good_token = False

        logger.debug(f'{str_token_search}, is_expired: {is_expired}, is_good_token: {is_good_token}')

        if not is_good_token:
            oauth_token_info = self.introspect(http_access_token)

            if oauth_token_info is None:
                logger.warning(self.make_log_msg('Introspection failed!'))
                return

            user = self.update_or_create_user(oauth_token_info)

            if user is None:
                logger.warning(self.make_log_msg('Cann\'t update or create user for %s' % oauth_token_info))
                return

            access = AccessToken.objects.save_token(
                user,
                oauth_token_info.get('access_token'),
                None,
                oauth_token_info.get('expires_at'),
            )
        else:
            if not access.is_external:
                logger.warning(self.make_log_msg('Access token is internal!'))
                return

        request.session[SESSION_OAUTH_TOKEN_ID] = access.id

        logger.debug(self.make_log_msg('User "%s" authenticated with bearer: %s' % (access.user, http_access_token)))

        return access.user

    def check_user_auth_validity(self, request):
        access_id = request.session.get(SESSION_OAUTH_TOKEN_ID)

        if not access_id:
            logger.warning(self.make_log_msg('There is no access token id in session for user %s.' % (request.user, )))
            return False

        try:
            access = AccessToken.objects.get(id=access_id, user=request.user)
        except AccessToken.DoesNotExist:
            logger.warning(self.make_log_msg('Access token not found %s (%s)!' % (access_id, request.user)))
            return False

        if not access.is_external:
            logger.warning(self.make_log_msg('Access token is internal!'))
            return

        logger.debug(self.make_log_msg('Access is_expired: %s (%s)' % (access.is_expired, access.expires_at)))
        return not access.is_expired


class OAuthBackend(OAuthBaseBackend):

    def authenticate(self, request, oauth_token_info=None):
        if oauth_token_info is None:
            return

        logger.debug(self.make_log_msg('Token info: %s' % oauth_token_info))

        user = self.update_or_create_user(oauth_token_info)

        if user is None:
            logger.debug(self.make_log_msg('Cann\'t update or create user for %s' % oauth_token_info))
            return

        access = AccessToken.objects.save_token(
            user,
            oauth_token_info.get('access_token'),
            oauth_token_info.get('refresh_token'),
            oauth_token_info.get('expires_at'),
        )

        request.session[SESSION_OAUTH_TOKEN_ID] = access.id

        logger.debug(self.make_log_msg('User "%s" authenticated with token info: %s' % (user, oauth_token_info)))

        return user

    def check_user_auth_validity(self, request):
        access_id = request.session.get(SESSION_OAUTH_TOKEN_ID)

        if not access_id:
            logger.warning(self.make_log_msg('There is no access token id in session for user %s.' % (request.user, )))
            return False

        try:
            access = AccessToken.objects.get(id=access_id, user=request.user)
        except AccessToken.DoesNotExist:
            logger.warning(self.make_log_msg('Access token not found %s (%s)!' % (access_id, request.user)))
            return False

        if access.is_expired:
            try:
                logger.debug(self.make_log_msg('Try refresh token with id %s' % (access_id, )))
                provider = get_oauth_provider()
                oaut_session = self.get_oauth_session(provider, token=access.get_requests_token_info())
                new_oauth_token_info = oaut_session.refresh_token(provider.access_token_url)

                user = self.update_or_create_user(new_oauth_token_info)
                if user is None:
                    return False

                logger.debug(self.make_log_msg('New token: %s' % new_oauth_token_info.get('access_token')))

                AccessToken.objects.update_token(
                    access,
                    new_oauth_token_info.get('access_token'),
                    new_oauth_token_info.get('refresh_token'),
                    new_oauth_token_info.get('expires_at'),
                )

                logger.debug('>>>> %s' % AccessToken.objects.find(new_oauth_token_info.get('access_token')))

            except Exception:
                logger.exception(self.make_log_msg('Try refresh token FAILD with id %s ' % (access_id, )))
                return False
        else:
            logger.debug(self.make_log_msg('Use current token with id %s' % (access_id, )))

        return True


class OAuthBearerOpenIdBackend(OAuthBearerBackend):

    def clean_user_guid(self, userinfo):
        return userinfo.get('sub')

    def clean_user_data(self, userinfo):
        username = userinfo.get('preferred_username')
        return {
            'username': username,
            'first_name': userinfo.get('given_name', username),
            'last_name': userinfo.get('family_name', username),
            'email': userinfo.get('email', ''),
        }

    def introspect(self, access_token):
        oauth_provider = get_oauth_provider()

        introspection_data = requests.post(
            oauth_provider.introspection_url,
            data={'token': access_token},
            auth=requests.auth.HTTPBasicAuth(oauth_provider.consumer_key, oauth_provider.consumer_secret)
        )

        introspection_data = introspection_data.json()

        logger.debug(self.make_log_msg('Introspect info: %s' % introspection_data))

        if introspection_data.get('active'):
            return {
                'access_token': access_token,
                'expires_at': introspection_data['exp']
            }


class OAuthOpenIdBackend(OAuthBackend):

    def clean_user_guid(self, userinfo):
        return userinfo.get('sub')

    def clean_user_data(self, userinfo):
        username = userinfo.get('preferred_username')
        return {
            'username': username,
            'first_name': userinfo.get('given_name', username),
            'last_name': userinfo.get('family_name', username),
            'email': userinfo.get('email', ''),
        }


class OAuthBearerOpenIdJwtBackend(OAuthBearerOpenIdBackend):

    LOGGER_MSG_PREFIX = 'Auth with  JWT Bearer'

    def get_userinfo(self, oauth_token_info):
        access_token = oauth_token_info['access_token']
        token_data = jwt.decode(access_token, verify=False)
        return token_data


class OAuthOpenIdJwtBackend(OAuthOpenIdBackend):

    LOGGER_MSG_PREFIX = 'Auth with JWT token info'

    def get_userinfo(self, oauth_token_info):
        access_token = oauth_token_info['access_token']
        token_data = jwt.decode(access_token, verify=False)
        return token_data


class OAuthNGIdBackend(OAuthBackend):

    def clean_user_guid(self, userinfo):
        return userinfo.get('nextgis_guid')

    def clean_user_data(self, userinfo):
        return {
            'username': userinfo.get('username'),
            'first_name': userinfo.get('first_name'),
            'last_name': userinfo.get('last_name'),
            'email': userinfo.get('email'),
            'locale': userinfo.get('locale'),
        }
