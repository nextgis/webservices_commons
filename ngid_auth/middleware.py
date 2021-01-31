import logging

import django.dispatch

from django.utils import timezone
from django.contrib.auth import login, logout, authenticate

from .mixins import OAuthClientMixin
from .provider import get_oauth_provider

user_plan_detected = django.dispatch.Signal(providing_args=["user", "plan"])


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
            except:
                pass
            finally:
                request.session['user_plan']= session_up_info


class OAuth2ResourceServerAuthenticationMiddleware(OAuthClientMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if request.META.get("HTTP_AUTHORIZATION", "").startswith("Bearer"):
                
                http_auth = request.META.get("HTTP_AUTHORIZATION")
                access_token = http_auth[len("Bearer"):].strip()

                oauth_token_info = {
                    'access_token': access_token
                }
                user = authenticate(request, oauth_token_info=oauth_token_info)
                    
                if user is not None:
                    login(request, user)
        
        response = self.get_response(request)
        
        return response
