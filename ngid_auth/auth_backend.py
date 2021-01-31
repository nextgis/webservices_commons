from __future__ import unicode_literals

import datetime
import jwt
import logging
import requests

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.dispatch import Signal
from django.utils import timezone
from django.utils.timezone import make_aware

from .models import AccessToken
from .mixins import OAuthClientMixin
from .provider import get_oauth_provider


UserModel = get_user_model()


signal_userinfo_got = Signal(providing_args=["user", "userinfo"])


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


class OAuthBackend(OAuthClientMixin, ModelBackend):

    def user_can_authenticate(self, user):
        result = super(OAuthBackend, self).user_can_authenticate(user)
        
        try:
            # access = AccessToken.objects.get(user_id=user.nextgis_guid).select_related('user')
            access = AccessToken.objects.filter(user_id=user.nextgis_guid).order_by('-id').select_related('user')[0]
        except AccessToken.DoesNotExist:
            result = False
        # except AccessToken.MultipleObjectsReturned:
        #     result = False
        else:
            logging.warning(timezone.now())
            logging.warning(access.expires_at)
            need_to_refresh = timezone.now() > access.expires_at
            if need_to_refresh:
                if access.refresh_token:
                    try:
                        provider = get_oauth_provider()
                        oaut_session = self.get_oauth_session(provider, token=access.get_requests_token_info())
                        new_oauth_token_info = oaut_session.refresh_token(provider.access_token_url)
                        
                        user = self.update_or_create_user(new_oauth_token_info)
                        if user is None:
                            result = False

                        access.update_with_requests_token_info(new_oauth_token_info)

                    except:
                        result = False
                else:
                    result = False


        return result

    def authenticate(self, request, oauth_token_info=None):    
        self.request = request

        if not oauth_token_info:
            return

        if 'refresh_token' not in oauth_token_info:
            oauth_token_info = self.introspect(oauth_token_info['access_token'])
        if not oauth_token_info:
            return

        user = self.update_or_create_user(oauth_token_info)

        if user is None:
            return

        defaults = {
            'user_id': user.nextgis_guid,
            'access_token': oauth_token_info['access_token'],
            'refresh_token': oauth_token_info.get('refresh_token'),
            'expires_at': make_aware(datetime.datetime.fromtimestamp(oauth_token_info['expires_at'])),
        }

        access, created = AccessToken.objects.update_or_create(
            defaults=defaults,
            user_id=user.nextgis_guid,
            access_token=oauth_token_info['access_token'],
        )

        return user

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

        signal_userinfo_got.send(sender=self.__class__, user=user, userinfo=userinfo)

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
            "username": userinfo.get('username'),
            "first_name": userinfo.get('first_name'),
            "last_name": userinfo.get('last_name'),
            "email": userinfo.get('email'),
        }


class OAuthOpenIdBackend(OAuthBackend):

    def clean_user_guid(self, userinfo):
        return userinfo.get('sub')

    def clean_user_data(self, userinfo):
        return {
            "username": userinfo.get('preferred_username'),
            "first_name": userinfo.get('given_name'),
            "last_name": userinfo.get('family_name'),
            "email": userinfo.get('email'),
        }

    def introspect(self, access_token):
        oauth_provider = get_oauth_provider()
            
        introspection_data = requests.post(
            oauth_provider.introspection_url,
            data={'token': access_token},
            auth=requests.auth.HTTPBasicAuth(oauth_provider.consumer_key, oauth_provider.consumer_secret)
        )
        
        introspection_data = introspection_data.json()

        if introspection_data.get('active'):
            return {
                'access_token': access_token,
                'expires_at': introspection_data['exp']
            }


class OAuthOpenIdJwtBackend(OAuthOpenIdBackend):

    def get_userinfo(self, oauth_token_info):
        access_token = oauth_token_info['access_token']
        token_data = jwt.decode(access_token, verify=False)
        return token_data


class OAuthNGIdBackend(OAuthBackend):

    def clean_user_guid(self, userinfo):
        return userinfo.get('nextgis_guid')
