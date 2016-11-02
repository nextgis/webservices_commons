from django import template
register = template.Library()

userreport_id = {
    'webgis_ru': '4b2c2642-596d-4185-816e-95a5374ee987',
    'webgis_en': '85e9ea99-8fad-4a9b-8cad-04b884e8901a',
}


@register.simple_tag
def get_userreport(app_name):
    return userreport_id[app_name] if app_name in userreport_id.keys() else ''
