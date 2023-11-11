from django.contrib import admin

from nextgis_common.ngid_auth.models import OAuthState, AccessToken


class OAuthStateAdmin(admin.ModelAdmin):
    list_display = ('value', 'client_id', 'created')
    search_fields = ('value', 'client_id')


class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'modified', 'expires_at', 'state', 'access_token', 'refresh_token', 'access_token_id')
    search_fields = ('access_token', 'refresh_token')


admin.site.register(OAuthState, OAuthStateAdmin)
admin.site.register(AccessToken, AccessTokenAdmin)
