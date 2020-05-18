from django.conf import settings
from .scopes import NextGisIdScopes

class NgidProvider:
    """Configuration for OAuth provider"""

    id = 'ngid_provider'
    name = 'NextGIS ID Provider'

    @staticmethod
    def authorization_url():
        return getattr(settings, 'NGID_AUTH_URL', 'https://my.nextgis.com/oauth2/authorize/')

    @staticmethod
    def access_token_url():
        return getattr(settings, 'NGID_TOKEN_URL', 'https://my.nextgis.com/oauth2/token/')

    @staticmethod
    def profile_url():
        return getattr(settings, 'NGID_PROFILE_URL', 'https://my.nextgis.com/api/v1/user_info/')

    @staticmethod
    def instance_url():
        return getattr(settings, 'NGID_PROFILE_URL', 'https://my.nextgis.com/api/v1/instance_info/')

    @staticmethod
    def consumer_key():
        return settings.NGID_CLIENT_ID

    @staticmethod
    def consumer_secret():
        return settings.NGID_CLIENT_SECRET

    @staticmethod
    def scopes():
        return getattr(settings, 'NGID_SCOPES', [NextGisIdScopes.USER_INFO_READ, ])

    @staticmethod
    def user_id():
        return 'nextgis_guid'
