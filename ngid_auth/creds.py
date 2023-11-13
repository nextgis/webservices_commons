from django.conf import settings
import json
from nextgis_common.ngid_auth.models import OAuthState


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
    def get_by_state(cls, state):
        creds = cls.get_default()
        st = OAuthState.objects.filter(value=state).first()
        if st:
            client_id = st.client_id
            crr = Creds.search(client_id=client_id)
            if crr:
                creds = crr
        return creds

    @classmethod
    def get_default(cls):
        cr = {
            'CLIENT_ID': settings.OAUTH_CLIENT_ID,
            'CLIENT_SECRET': settings.OAUTH_CLIENT_SECRET
        }
        return cr

    @classmethod
    def is_default(cls, state):
        obj = OAuthState.objects.filter(value=state).first()
        if obj:
            if obj.client_id == settings.OAUTH_CLIENT_ID:
                return True
        return False
