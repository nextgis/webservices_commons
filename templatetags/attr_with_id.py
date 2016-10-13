from django import template
from widget_tweaks.templatetags.widget_tweaks import silence_without_field, append_attr

register = template.Library()


@register.filter(name='attr_with_id')
@silence_without_field
def attr_with_id(field, attr):
    attr = attr.replace('$id', field.auto_id)
    return append_attr(field, attr)


