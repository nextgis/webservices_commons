from django.conf import settings
import json


#
# TODO: дублируется функционал класса OAuthProvider ?
#
class Creds:

    @classmethod
    def get_all(cls):
        creds = settings.NGW_CREDENTIALS_FOR_TOOLS
        creds = json.loads(creds)
        return creds

    @classmethod
    def search(cls, client_id=None, operation_id=None):
        creds = cls.get_all()
        for cr in creds:
            if client_id:
                if cr.get('CLIENT_ID') == client_id:
                    return cr

            if operation_id:
                if cr.get('OPERATION_ID') == operation_id:
                    return cr
        return None

    @classmethod
    def get_default(cls):
        cr = {
            'CLIENT_ID': settings.OAUTH_CLIENT_ID,
            'CLIENT_SECRET': settings.OAUTH_CLIENT_SECRET
        }
        return cr
