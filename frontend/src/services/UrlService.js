const urls = {
  'nextgis_site': {
    'en': 'https://nextgis.com',
    'ru': 'https://nextgis.ru'
  }
};

export function getUrlByLocale(name, locale) {
  return urls[name] ? urls[name][locale] : '#';
}