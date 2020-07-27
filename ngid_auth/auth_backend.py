from __future__ import unicode_literals

from django.contrib.auth.backends import ModelBackend
from .models import AccessToken


class NgidBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        try:
            nguid = kwargs.get('nguid')
            access_token = kwargs.get('access_token')

            access = AccessToken.objects.filter(user_id=nguid, access_token=access_token).select_related('user')[0]
        except IndexError:
            return None
        else:
            return access.user
