from django.utils import translation


def activate_user_locale(request, user_locale):
    translation.activate(user_locale)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_locale
    #response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_locale)

