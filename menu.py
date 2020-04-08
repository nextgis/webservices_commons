import json

from django.conf import settings
from django.urls import reverse, resolve
from django.utils.translation import get_language


class Menu(object):
    """docstring for Menu"""
    def __init__(self, user):
        super(Menu, self).__init__()
        
        cur_lang = get_language()

        menu_options = getattr(settings, 'NEXTGISID_MENU', {})
        self.menu = []
        for url_name, options in menu_options.items():
            view = resolve(reverse(url_name)).func.view_class
            if hasattr(view, 'is_available_for_user') and view.is_available_for_user(user):
                self.menu.append({
                    'id': url_name,
                    'link': reverse(url_name),
                    'text': self.get_menu_title(options, cur_lang) or url_name,
                })

    def get_menu_title(self, options, lang):
        title_variants = options.get('title', {})

        title = title_variants.get(lang)
        if title is None:
            title = title_variants.get('en')

        return title

    def get_menu_js_struct(self):
        return json.dumps(self.menu)
    

def get_menu(request):
    m = Menu(request.user)

    return {
        'MENU_JS_STRUCT': m.get_menu_js_struct(),
        'MENU_ACTIVE_ITEM_ID': request.resolver_match.url_name,
    }
