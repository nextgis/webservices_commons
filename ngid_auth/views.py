from __future__ import unicode_literals

import logging

from django.utils.crypto import constant_time_compare
from requests_oauthlib import OAuth2Session

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import RedirectView, View

from nextgis_common.ngid_auth.ngid_provider import NgidProvider
from nextgis_common.utils import activate_user_locale
from .models import AccessToken


logger = logging.getLogger('nextgis_common.auth')


class OAuthClientMixin(object):

    def get_oauth_session(self, provider):
        oaut_session = OAuth2Session(
            client_id=provider.consumer_key(),
            scope=provider.scopes()
        )
        oaut_session.redirect_uri = self.get_callback_url
        return oaut_session

    @property
    def session_key(self):
        return 'request-state-ngid'

    @property
    def application_state(self):
        return self.request.session.get(self.session_key, None)

    @application_state.setter
    def application_state(self, state):
        self.request.session[self.session_key] = state

    @property
    def get_callback_url(self):
        callback_path = str(reverse_lazy(NgidOAuth2CallbackView.view_name))
        callback_url = self.request.build_absolute_uri(callback_path)
        return callback_url


class NgidOAuth2LoginView(OAuthClientMixin, RedirectView):
    view_name = 'ngid_login'

    permanent = False

    def get_redirect_url(self, **kwargs):
        provider = NgidProvider
        oaut_session = self.get_oauth_session(provider)
        authorization_url, state = oaut_session.authorization_url(provider.authorization_url())
        self.application_state = state # save state key for check
        return authorization_url


class NgidOAuth2CallbackView(OAuthClientMixin, View):
    view_name = 'ngid_callback'

    def get(self, request, *args, **kwargs):
        provider = NgidProvider

        # Fetch access token
        oaut_session = self.get_oauth_session(provider)

        raw_token = oaut_session.fetch_token(
            provider.access_token_url(),
            client_id=provider.consumer_key(),
            client_secret=provider.consumer_secret(),
            state=self.application_state,
            scope=provider.scopes(),
            authorization_response=request.build_absolute_uri(request.get_full_path()),
        )

        if raw_token is None:
            return self.handle_login_failure(provider, 'Could not retrieve token')

        # Fetch profile info
        info_raw_resp = oaut_session.get(provider.profile_url())
        info_raw_resp.raise_for_status()
        info = info_raw_resp.json() or info_raw_resp.text

        if info is None:
            return self.handle_login_failure(provider, 'Could not retrieve profile')
        identifier = self.get_user_id(provider, info)
        if identifier is None:
            return self.handle_login_failure(provider, 'Could not determine id')

        # Get or create access record
        defaults = {
            'access_token': raw_token['access_token'],
            'refresh_token': raw_token['refresh_token'],
        }
        access, created = AccessToken.objects.get_or_create(
             user_id=identifier, defaults=defaults
        )
        if not created:
            access.access_token = raw_token['access_token']
            access.refresh_token = raw_token['refresh_token']
            #TODO: access.expires_in
            access.save()

        # Handle user
        user = authenticate(nguid=identifier, access_token=raw_token['access_token'])

        if user is None:
            return self.handle_new_user(access, info)
        else:
            return self.handle_existing_user(user, info)

    def get_error_redirect(self, provider, reason):
        return settings.LOGIN_URL

    def get_login_redirect(self):
        return settings.LOGIN_REDIRECT_URL

    def create_user(self, info):
        user_model = get_user_model()
        kwargs = info
        kwargs['password'] = None
        return user_model.objects.create_user(**kwargs)

    def update_user(self, user, info):
        try:
            user_model = get_user_model()
            model_obj = user_model.objects.filter(nextgis_guid=user.nextgis_guid)
            model_obj.update(**info)

            user.refresh_from_db()
        except Exception as ex:
            logger.critical('Error on user %s update: %s', user.nextgis_guid, ex.message)


    def get_user_id(self, provider, info):
        """Return unique identifier from the profile info"""
        id_key = provider.user_id() or 'id'
        result = info
        try:
            for key in id_key.split('.'):
                result = result[key]
            return result
        except KeyError:
            return None

    def handle_login_failure(self, provider, reason):
        """Message user and redirect on error"""
        logger.error('Authenication Failure: {0}'.format(reason))
        messages.error(self.request, 'Authenication Failed')
        return redirect(self.get_error_redirect(provider, reason))

    def handle_existing_user(self, user, info):
        """Login user, update and redirect"""
        self.update_user(user, info)
        login(self.request, user)
        activate_user_locale(self.request, user.locale)
        return redirect(self.get_login_redirect())

    def handle_new_user(self, access, info):
        """Create a shell auth.User and redirect"""
        user = self.create_user(info)
        # update token record
        access.user = user
        access.save()
        # auth and login
        user = authenticate(nguid=user.nextgis_guid, access_token=access.access_token)
        login(self.request, user)
        activate_user_locale(self.request, user.locale)
        return redirect(self.get_login_redirect())


class NgidLogoutView(View):
    view_name = 'ngid_logout'

    def get(self, request, *args, **kwargs):
        #TODO: logout on my.nextgis.com?
        if request.user.is_authenticated():
            logout(request)
        return redirect(settings.LOGIN_REDIRECT_URL)