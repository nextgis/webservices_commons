from __future__ import unicode_literals

from django.conf import settings

without_accesstoken = False
if hasattr(settings, 'IS_DISABLED_COMMON_ACCESSTOKEN'):
    if settings.IS_DISABLED_COMMON_ACCESSTOKEN:
        without_accesstoken = True

if not without_accesstoken:
    from nextgis_common.ngid_auth.models import AccessToken
