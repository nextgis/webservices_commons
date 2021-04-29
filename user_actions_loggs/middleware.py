import json
import logging

from django.urls import resolve
from django.utils import timezone

logger = logging.getLogger('nextgis_common.user_actions_logging')


class UserActionsLogging():
    
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        
        data = {
            '@timestamp': timezone.now().utcnow().isoformat(),
            'request': {
                'method': request.method,
                'path': request.path,
                'query_string': request.GET.urlencode(),
                'remote_addr': request.META['HTTP_HOST'],
                'get_host': request.get_host(),
            },
             'response': {
                'route_name': resolve(request.path_info).url_name,
                'status_code': response.status_code,
            },
            'user': None,
            'context': None,

        }

        if request.user.is_authenticated:
            data['user'] = {
                'id': request.user.id,
                'keyname': request.user.username,
                'display_name': '%s %s' % (request.user.first_name, request.user.last_name),
                'oauth_subject': getattr(request.user, 'oauth_subject', None)
            }
        
        logger.info(json.dumps(data))


        # Code to be executed for each request/response after
        # the view is called.

        return response
