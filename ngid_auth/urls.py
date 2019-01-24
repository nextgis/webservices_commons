from django.conf.urls import url
from nextgis_common.ngid_auth.views import NgidOAuth2CallbackView, NgidOAuth2LoginView, NgidLogoutView

urlpatterns = [
    url('^login/$', NgidOAuth2LoginView.as_view(), name=NgidOAuth2LoginView.view_name),
    url('^login/callback/$', NgidOAuth2CallbackView.as_view(), name=NgidOAuth2CallbackView.view_name),
    url('^logout/$', NgidLogoutView.as_view(), name=NgidLogoutView.view_name)
]

