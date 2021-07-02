import logging

import django.dispatch

from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import (
    BACKEND_SESSION_KEY,
    load_backend,
)
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from .mixins import OAuthClientMixin
from .provider import get_oauth_provider

user_plan_detected = django.dispatch.Signal(providing_args=["user", "plan"])


logger = logging.getLogger(__name__)


class UserPlan(OAuthClientMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        is_user_auth_before_response_gen = request.user.is_authenticated

        if is_user_auth_before_response_gen:
            self.get_plan(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        if not is_user_auth_before_response_gen and request.user.is_authenticated:
            self.get_plan(request)

        return response

    def get_plan(self, request):
        session_up_info = request.session.get('user_plan', {})

        self.request = request

        if session_up_info.get('last_check_date', 0) < request.user.last_login.timestamp():
            try:
                oauth_provider = get_oauth_provider()
                oauth_session = self.get_oauth_session(oauth_provider)
                ngid_up_info = oauth_session.get(oauth_provider.instance_url()).json()
                ngid_user_plan = ngid_up_info.get('plan_id')

                session_up_info['last_check_date'] = timezone.now().timestamp()

                if session_up_info.get('plan', '') != ngid_user_plan:
                    session_up_info['plan'] = ngid_user_plan

                    user_plan_detected.send(sender=self.__class__, user=request.user, plan=ngid_user_plan)
            except Exception:
                pass
            finally:
                request.session['user_plan'] = session_up_info


class HttpAuthorizationUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            user = authenticate(request)

            if user is not None:
                login(request, user)


class NgPostAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                backend_path = request.session[BACKEND_SESSION_KEY]
            except KeyError:
                pass
            else:
                if backend_path in settings.AUTHENTICATION_BACKENDS:
                    backend = load_backend(backend_path)

                    if hasattr(backend, 'check_user_auth_validity'):
                        if not backend.check_user_auth_validity(request):
                            logout(request)
