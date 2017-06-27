from django import template
register = template.Library()

chatra_groupid = {
    'webgis': '3RwjGShJZswB4zHed',
    'qms': 'rxqAGPoDckSDptYt9',
}


@register.simple_tag
def get_chatra_groupid(app_name):
    return chatra_groupid[app_name] if app_name in chatra_groupid.keys() else 'sdfds'
