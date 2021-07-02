from django.conf import settings

from .provider import OAuthProvider
from .scopes import NextGisIdScopes


class NgidProvider(OAuthProvider):
    """Configuration for OAuth provider"""

    id = 'ngid_provider'
    name = 'NextGIS ID Provider'

    @staticmethod
    def get_authorization_url():
        return getattr(settings, 'NGID_AUTH_URL', 'https://my.nextgis.com/oauth2/authorize/')

    @staticmethod
    def get_access_token_url():
        return getattr(settings, 'NGID_TOKEN_URL', 'https://my.nextgis.com/oauth2/token/')

    @staticmethod
    def get_profile_url():
        return getattr(settings, 'NGID_PROFILE_URL', 'https://my.nextgis.com/api/v1/user_info/')

    @staticmethod
    def get_instance_url():
        return getattr(settings, 'NGID_PROFILE_URL', 'https://my.nextgis.com/api/v1/instance_info/')

    @staticmethod
    def get_consumer_key():
        return settings.NGID_CLIENT_ID

    @staticmethod
    def get_consumer_secret():
        return settings.NGID_CLIENT_SECRET

    @staticmethod
    def get_scopes():
        return getattr(settings, 'NGID_SCOPES', [NextGisIdScopes.USER_INFO_READ, ])

    @staticmethod
    def get_user_id():
        return 'nextgis_guid'


    def __init__(self):
        super(NgidProvider, self).__init__()

        self.user_id = self.get_user_id()


    def manage_userinfo(self, info):
        attrs = dict()
        attrs['username'] = info.get('username')

        attrs['nextgis_guid'] = info.get(self.user_id)
        attrs['first_name'] = info.get('first_name')
        attrs['last_name'] = info.get('last_name')

        return attrs