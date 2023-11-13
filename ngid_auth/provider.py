from django.conf import settings
from django.utils.module_loading import import_string


def get_oauth_provider(creds=None):
    provider_class = import_string(
        getattr(settings, 'OAUTH_PROVIDER', 'nextgis_common.ngid_auth.provider.OAuthProvider')
    )
    return provider_class(creds=creds)



class OAuthProvider:
    """Configuration for OAuth provider"""

    id = 'auth_provider'
    name = 'Common OAuth Provider'

    @staticmethod
    def get_authorization_url():
        return getattr(settings, 'OAUTH_AUTHORIZATION_URL')

    @staticmethod
    def get_access_token_url():
        return getattr(settings, 'OAUTH_TOKEN_URL')

    @staticmethod
    def get_introspection_url():
        return getattr(settings, 'OAUTH_SERVER_INTROSPECTION')

    @staticmethod
    def get_profile_url():
        return getattr(settings, 'OAUTH_USERINFO_URL')

    @staticmethod
    def get_consumer_key():
        return settings.OAUTH_CLIENT_ID

    @staticmethod
    def get_consumer_secret():
        return settings.OAUTH_CLIENT_SECRET

    @staticmethod
    def get_logout_url():
        return getattr(settings, 'OAUTH_LOGOUT_URL', None)

    @staticmethod
    def get_scopes():
        return getattr(settings, 'OAUTH_SCOPES', None)


    def __init__(self, creds=None):
        self.authorization_url = self.get_authorization_url()
        self.access_token_url = self.get_access_token_url()
        self.profile_url = self.get_profile_url()
        self.introspection_url = self.get_introspection_url()
        self.logout_url = self.get_logout_url()
        if creds:
            self.consumer_key = creds.get('CLIENT_ID')
            self.consumer_secret = creds.get('CLIENT_SECRET')
        else:
            self.consumer_key = self.get_consumer_key()
            self.consumer_secret = self.get_consumer_secret()

        self.scopes = self.get_scopes()

        self.user_id = 'sub'


    def manage_userinfo(self, info):
        attrs = dict()

        attrs['username'] = info.get('preferred_username')

        attrs['nextgis_guid'] = info.get(self.user_id)
        attrs['first_name'] = info.get('given_name')
        attrs['last_name'] = info.get('family_name')

        return attrs

