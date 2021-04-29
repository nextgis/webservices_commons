import json

from django.conf import settings
from django.urls import reverse, resolve
from django.utils.translation import get_language


class Menu(object):
    """docstring for Menu"""
    def __init__(self, user):
        super(Menu, self).__init__()

        cur_lang = get_language()

        menu_options = getattr(settings, 'NEXTGISID_MENU', [])
        self.menu = []
        for menu_item in menu_options:
            url_name = menu_item.get('url_name')
            view = resolve(reverse(url_name)).func.view_class
            if hasattr(view, 'is_available_for_user') and not view.is_available_for_user(user):
                pass
            else:

                self.menu.append({
                    'id': url_name,
                    'link': reverse(url_name),
                    'text': self.get_menu_title(menu_item, cur_lang) or url_name,
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
    resolver_match = request.resolver_match
    menu_active_item_id = ''
    if resolver_match:
        menu_active_item_id = request.resolver_match.url_name
     
    return {
        'MENU_JS_STRUCT': m.get_menu_js_struct(),
        'MENU_ACTIVE_ITEM_ID': menu_active_item_id,
    }
