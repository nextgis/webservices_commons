from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class AccessToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, to_field='nextgis_guid')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    access_token = models.CharField(max_length=4096, blank=True, null=True, default=None)
    refresh_token = models.CharField(max_length=4096, blank=True, null=True, default=None)
    expires_in = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{0} {1}'.format(self.user, self.access_token)
