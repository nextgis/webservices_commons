# NextGIS Commons
Django app with common parts from web services


## Requirements

### Python
```
django-gravatar2>=1.4.0
django-widget-tweaks>=1.4.1
```

If NGID OAuth client will be used:
```
requests>=2.11.1,<=2.12
requests_oauthlib=0.7.0
```

### JS
```
TODO
```


## Add to new service project

```
git clone https://github.com/nextgis/webservices_commons nextgis_common
```
or
```
git submodule add https://github.com/nextgis/webservices_commons nextgis_common
```

Add to INSTALLED_APPS:
```
    'widget_tweaks',
    'django_gravatar',
    'nextgis_common',
```

## Usage NGID OAuth authorization
### Create APP on my.nextgis.com
**Client type**: confidential

**Authorization Grant Type**: authorization-code

**Redirect Uris**: http://your_site_url/login/callback/

**Skip authorization**: True


### Modify settings.py
Add to _AUTHENTICATION_BACKENDS_:
```
AUTHENTICATION_BACKENDS = (
    ...
    ... 
    'nextgis_common.ngid_auth.auth_backend.NgidBackend',
)
```



### Append urls to urls.py
```
urlpatterns = [
    ... 
    ...
    url(r'', include('nextgis_common.ngid_auth.urls')),
]
```

### Update DB
```
manage.py migrate
```
 
### Use links for login\logout in templates:
For example:
```
<a href="{% url 'ngid_login' %}">{% trans 'Sign in'%}</a>
```

```
<a href="{% url 'ngid_logout' %}">{% trans 'Log out'%}</a>
```

## Struct
TODO