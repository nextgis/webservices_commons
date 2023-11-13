from __future__ import unicode_literals

import logging
import urllib.parse

from django.db import transaction

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import RedirectView, View

from nextgis_common.ngid_auth.provider import get_oauth_provider
from nextgis_common.utils import activate_user_locale

from .creds import Creds
from .mixins import OAuthClientMixin
from .models import OAuthState

logger = logging.getLogger('nextgis_common.auth')


class NgidOAuth2LoginView(OAuthClientMixin, RedirectView):
    view_name = 'ngid_login'
    permanent = False

    def get_redirect_url(self, **kwargs):
        provider = get_oauth_provider(self._creds)

        oaut_session = self.get_oauth_session(provider)
        authorization_url, state = oaut_session.authorization_url(provider.authorization_url)
        st = OAuthState(value=state, client_id=self._client_id)
        st.save()
        # print(f'authorization_url: {authorization_url}, state: {state}')
        logger.info(f'authorization_url: {authorization_url}, state: {state}')
        self.application_state = state  # save state key for check
        if 'next' in self.request.GET:  # save 'next' url
            self.application_next_url = self.request.GET['next']
        logger.info(f'REDIRECT_URL: {authorization_url}')
        return authorization_url

    def _get_redirect_url(self):
        try:
            rl = reverse_lazy(NgidOAuth2CallbackView.view_name)
            sstr = str(rl)
            rr_url = self.request.build_absolute_uri(sstr)
        except Exception as e:
            logger.exception(e)
        return rr_url

    def get(self, request, *args, **kwargs):
        client_id = request.GET.get('client_id')
        self._creds = Creds.get_default()
        if client_id:
            self._creds = Creds.search(client_id=client_id)
        return super().get(request, *args, **kwargs)


class NgidOAuth2CallbackView(OAuthClientMixin, View):
    view_name = 'ngid_callback'

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        try:
            provider = get_oauth_provider()
            state = request.GET.get('state')

            # Fetch access token
            oaut_session = self.get_oauth_session(provider)

            absolute_uri = request.build_absolute_uri(request.get_full_path())
            # TODO: refactor: quick fix
            if 'https' not in absolute_uri:
                absolute_uri = absolute_uri.replace('http', 'https')
            dd_url = '/login/callback/'

            logger.info(f'{dd_url} : fetching token: provider.access_token_url: {provider.access_token_url}, '
                        f'client_id: {provider.consumer_key}, '
                        f'client_secret: {provider.consumer_secret}, '
                        f'state: {state}, '
                        f'scope: {provider.scopes}, '
                        f'authorization_response: {absolute_uri}'
            )
            client_id = provider.consumer_key
            client_secret = provider.consumer_secret
            st = OAuthState.objects.filter(value=state).first()
            if st:
                client_id = st.client_id
                crr = Creds.search(client_id=client_id)
                client_secret = crr.get('CLIENT_SECRET')

            raw_token = oaut_session.fetch_token(
                provider.access_token_url,
                client_id=client_id,
                client_secret=client_secret,
                state=state,
                scope=provider.scopes,
                authorization_response=absolute_uri,
            )

            if raw_token is None:
                return self.handle_login_failure(provider, 'Could not retrieve token')

            user = authenticate(request, oauth_token_info=raw_token)

            if user is not None:
                login(self.request, user)
                activate_user_locale(self.request, user.locale)

            rr = self.get_login_redirect()
            rrr = redirect(rr)
        except Exception as e:
            logger.exception(e)
        return rrr

    def _get_redirect_url(self):
        try:
            rl = reverse_lazy(NgidOAuth2CallbackView.view_name)
            sstr = str(rl)
            rr_url = self.request.build_absolute_uri(sstr)
            logger.info(f'_got redirect url: {rr_url} ({sstr})')
        except Exception as e:
            logger.exception(e)
        return rr_url

    def get_error_redirect(self, provider, reason):
        return settings.LOGIN_URL

    def get_login_redirect(self):
        return self.application_next_url or settings.LOGIN_REDIRECT_URL

    def handle_login_failure(self, provider, reason):
        """Message user and redirect on error"""
        logger.error('Authenication Failure: {0}'.format(reason))
        messages.error(self.request, 'Authenication Failed')
        return redirect(self.get_error_redirect(provider, reason))


class NgidLogoutView(View):
    view_name = 'ngid_logout'

    def get(self, request, *args, **kwargs):
        #TODO: logout on my.nextgis.com?
        provider = get_oauth_provider()

        is_it_redirect_from_auth_server_logout = request.session.get('from_auth_server_asked', False) # request.GET.get('from_auth_server')

        if provider.logout_url and is_it_redirect_from_auth_server_logout is False:
            callback_path = '%s' % (str(reverse_lazy(self.view_name)), )
            request.session['from_auth_server_asked'] = True
            return redirect(
                '%s?%s' % (provider.logout_url, urllib.parse.urlencode({'redirect_uri': request.build_absolute_uri(callback_path)}))
            )
        else:
            request.session['from_auth_server_asked'] = False

        if request.user.is_authenticated:
            logout(request)

        return redirect(settings.LOGIN_REDIRECT_URL)