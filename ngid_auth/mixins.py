from __future__ import unicode_literals

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import os
import logging

logger = logging.getLogger('nextgis_common.ngid_auth.backands')


class OAuthClientMixin(object):

    @classmethod
    def do_get_oauth_session(cls, provider, token=None, scope=None):
        cl_id = provider.consumer_key
        cl_se = provider.consumer_secret
        extra = {
            'client_id': cl_id,
            'client_secret': cl_se,
        }
        verify = os.getenv('SSL_VERIFY', False)
        if not verify:
            verify = False
        scp = scope or provider.scopes
        r_url = provider.access_token_url
        oaut_session = OAuth2Session(
            client_id=cl_id,
            scope=scp,
            token=token,
            auto_refresh_url=r_url,
            auto_refresh_kwargs=extra,
        )
        logger.info(f'do_get_oauth_session(): '
                    f'client_id: {cl_id}, '
                    f'scope: {scp}, '
                    f'auto_refresh_url: {r_url}, '
                    f'auto_refresh_kwargs: {extra}, '
                    f'token: {token}'
                    )
        oaut_session.verify = verify
        oaut_session.redirect_uri = None
        return oaut_session

    def get_oauth_session(self, provider, token=None, scope=None):
        s = self.do_get_oauth_session(provider, token, scope)
        s.redirect_uri = self._get_redirect_url()
        return s

    def get_oauth_session_for_client(self, provider):
        client = BackendApplicationClient(client_id=provider.consumer_key)
        return OAuth2Session(client=client)

    def _get_redirect_url(self):
        return None

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
    def next_key(self):
        return 'request-next-ngid'

    @property
    def application_next_url(self):
        return self.request.session.get(self.next_key, None)

    @application_next_url.setter
    def application_next_url(self, url):
        self.request.session[self.next_key] = url
