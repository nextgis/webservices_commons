const urls = {
  'nextgis_site': {
    'en': 'https://nextgis.com',
    'ru': 'https://nextgis.ru'
  },
  'root': {
    'en': `${window.root_url}en`,
    'ru': `${window.root_url}ru`,
  },
  'ngid_login': window.ngid_login_url
};

export function getUrlByLocale(name, locale) {
  return urls[name] ? urls[name][locale] : '#';
}

export function getUrl(name) {
  return urls[name] || '#';
}