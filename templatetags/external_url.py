from django import template
register = template.Library()

external_links = {
    'nextgis_online': 'http://online.nextgis.com',
    'my_nextgis': 'https://my.nextgis.com',

    'nextgis_com_en': 'http://nextgis.com',
    'nextgis_com_ru': 'http://nextgis.ru',

    'terms_ru': 'http://nextgis.ru/terms/',
    'terms_en': 'http://nextgis.com/terms/',

    'privacy_ru': 'http://nextgis.ru/privacy',
    'privacy_en': 'http://nextgis.com/privacy',

    'docs_ru': 'http://docs.nextgis.ru',
    'docs_en': 'http://docs.nextgis.com',

    # temporary?
    'ngid_profile': 'https://my.nextgis.com/profile',
    'ngid_public_profile': 'https://my.nextgis.com/public_profile',
    'webgis': 'https://my.nextgis.com/webgis',

}

external_link_lang_default = 'en'


@register.simple_tag
def external_url(url_name, lang):
    
    external_link = external_links.get(
        '%s_%s' % (url_name, lang),
        external_links.get(
            '%s_%s' % (url_name, external_link_lang_default),
            ''
        )
    )

    return external_link
