from __future__ import unicode_literals

import datetime
import six

from hashlib import sha512

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import make_aware, utc

try:
    from django.utils.encoding import python_2_unicode_compatible
except ImportError as er:
    from six import python_2_unicode_compatible

MAX_TOKEN_LENGTH = 254


class AccessTokenManager(models.Manager):
    def get_access_token_id(self, access_token):
        if len(access_token) > MAX_TOKEN_LENGTH:
            access_token_id = 'sha512:' + sha512(six.ensure_binary(
                access_token)
            ).hexdigest()
        else:
            access_token_id = access_token

        return access_token_id

    def update_token(self, token, access_token, refresh_token, expires_at_utc):
        access_token_id = self.get_access_token_id(access_token)

        token.access_token_id = access_token_id
        token.access_token = access_token
        token.refresh_token = refresh_token
        token.expires_at = make_aware(
            datetime.datetime.fromtimestamp(expires_at_utc),
            timezone=utc,
        )

        token.save()

    def save_token(self, user, access_token, refresh_token, expires_at_utc, state=None):

        access_token_id = self.get_access_token_id(access_token)

        token = self.model(user=user, access_token_id=access_token_id)

        token.access_token_id = access_token_id
        token.access_token = access_token
        token.refresh_token = refresh_token
        token.expires_at = make_aware(
            datetime.datetime.fromtimestamp(expires_at_utc),
            timezone=utc,
        )
        if state:
            oo = OAuthState.objects.filter(value=state).first()
            if oo:
                token.state = oo
        token.save()

        return token

    def find(self, access_token):
        access_token_id = self.get_access_token_id(access_token)

        try:
            return self.get(access_token_id=access_token_id)
        except self.model.DoesNotExist:
            pass


class OAuthState(models.Model):
    value = models.TextField(primary_key=True)
    client_id = models.TextField(blank=True, null=True, default=None, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)


@python_2_unicode_compatible
class AccessToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, to_field='nextgis_guid', related_name='client_access_token')
    access_token_id = models.CharField(max_length=MAX_TOKEN_LENGTH, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    access_token = models.TextField(blank=True, null=True, default=None)
    refresh_token = models.TextField(blank=True, null=True, default=None)
    expires_at = models.DateTimeField(blank=True, null=True, db_index=True)
    state = models.ForeignKey(OAuthState, null=True, blank=True, on_delete=models.CASCADE,
                             to_field='value', related_name='oauth_state')

    objects = AccessTokenManager()

    def __str__(self):
        return '{0} {1}'.format(self.user, self.access_token)

    class Meta:
        index_together = [
            ("user", "access_token_id"),
        ]

    def save(self, *args, **kwargs):
        if not self.access_token_id and self.access_token:
            if len(self.access_token) > MAX_TOKEN_LENGTH:
                self.access_token_id = sha512(
                    six.ensure_binary(self.access_token)
                ).hexdigest()
            else:
                self.access_token_id = self.access_token

        super().save(*args, **kwargs)

    def get_requests_token_info(self):
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_at': self.expires_at.timestamp(),
        }

    def update_with_requests_token_info(self, requests_token_info):
        self.access_token = requests_token_info.get('access_token')
        self.refresh_token = requests_token_info.get('refresh_token')
        self.expires_at = make_aware(
            datetime.datetime.fromtimestamp(requests_token_info.get('expires_at')),
            timezone=utc,
        )

        self.save()

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def is_external(self):
        return self.refresh_token is None

    @classmethod
    def get_one_actual(cls, client_id):
        curr_timezone = timezone.get_current_timezone()
        ts_now = datetime.now(tz=curr_timezone)

        token = AccessToken.objects\
            .filter(state__client_id=client_id)\
            .filter(expires_at__lt=ts_now)\
            .order_by('-expires_at')\
            .first()

        return token

    @classmethod
    def get_many_expiring(cls, exclude_client):
        curr_timezone = timezone.get_current_timezone()
        ts_now = datetime.datetime.now(tz=curr_timezone)
        ts_refresh_after = ts_now - datetime.timedelta(seconds=settings.NGW_REFRESH_TOKENS_BEFORE_SECONDS)

        tokens = AccessToken.objects \
            .filter(expires_at__range=(ts_refresh_after, ts_now)) \
            .exclude(state__client_id=exclude_client) \
            .order_by('-expires_at')

        return tokens

