from nextgis_common.ngid_auth.auth_backend import OAuthOpenIdJwtBackend
from nextgis_common.ngid_auth.auth_backend import OAuthBearerOpenIdJwtBackend


class BlitzJwtBackend(OAuthOpenIdJwtBackend):
    USER_BIND_TYPE = 'username'
    FIELD_PREFERRED_USERNAME = 'sub'


class BlitzBearerBackend(OAuthBearerOpenIdJwtBackend):
    USER_BIND_TYPE = 'username'
    FIELD_PREFERRED_USERNAME = 'sub'
