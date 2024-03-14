from django.utils import translation
from django.conf import settings
from urllib.parse import urlparse

def activate_user_locale(request, user_locale):
    translation.activate(user_locale)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_locale
    #response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_locale)


def sanitize_url(url):
    allowed_hosts = settings.ALLOWED_HOSTS
    parsed = urlparse(url)
    if parsed.netloc:
        if parsed.netloc not in allowed_hosts:
            print('suspicious domain detected')
            return '/'
    return url

