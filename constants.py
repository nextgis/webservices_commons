from django.conf import settings

def get_constants(request):
	return {
		'EXTERNAL_URLS_DISABLED': getattr(settings, 'EXTERNAL_URLS_DISABLED', 'True'),
    'PROFILE_IN_NEW_TAB': getattr(settings, 'PROFILE_IN_NEW_TAB', True)
	}