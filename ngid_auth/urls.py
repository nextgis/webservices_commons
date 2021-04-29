from django.conf import settings
from django.conf.urls import url
from nextgis_common.ngid_auth.views import NgidOAuth2CallbackView, NgidOAuth2LoginView, NgidLogoutView


prefix = getattr(settings, 'OAUTH_URLS_PREFIX', '')


def get_url_pattern(base_url_pattern):
	return '^%s/%s/$' % (prefix, base_url_pattern) if prefix else '^%s/$' % base_url_pattern


urlpatterns = [
    url(get_url_pattern('login'), NgidOAuth2LoginView.as_view(), name=NgidOAuth2LoginView.view_name),
    url(get_url_pattern('login/callback'), NgidOAuth2CallbackView.as_view(), name=NgidOAuth2CallbackView.view_name),
    url(get_url_pattern('logout'), NgidLogoutView.as_view(), name=NgidLogoutView.view_name)
]

