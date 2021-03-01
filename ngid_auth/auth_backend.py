from __future__ import unicode_literals

import datetime
import jwt
import logging
import requests

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.dispatch import Signal
from django.utils import timezone
from django.utils.timezone import make_aware

from .models import AccessToken
from .mixins import OAuthClientMixin
from .provider import get_oauth_provider


UserModel = get_user_model()


signal_userinfo_got = Signal(providing_args=["user", "userinfo"])


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
