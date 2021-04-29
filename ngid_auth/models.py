from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.db import models
from django.utils.timezone import make_aware

try:
    from django.utils.encoding import python_2_unicode_compatible
except ImportError as er:
    from six import python_2_unicode_compatible

@python_2_unicode_compatible
class AccessToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, to_field='nextgis_guid', related_name='client_access_token')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    access_token = models.CharField(max_length=4096, blank=True, null=True, default=None)
    refresh_token = models.CharField(max_length=4096, blank=True, null=True, default=None)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{0} {1}'.format(self.user, self.access_token)

    class Meta:
        index_together = [
            ("user", "access_token"),
        ]

    def get_requests_token_info(self):
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_at': self.expires_at.timestamp(),
        }

    def update_with_requests_token_info(self, requests_token_info):
        self.access_token = requests_token_info.get('access_token')
        self.refresh_token = requests_token_info.get('refresh_token')
        self.expires_at = make_aware(datetime.datetime.fromtimestamp(requests_token_info.get('expires_at')))

        self.save()