import sib_api_v3_sdk as sib
from sib_api_v3_sdk.rest import ApiException
from . import my_secret_key as mykey


class SibContact():
    def __init__(self, email):
        self.email = email
        self.cfg = sib.Configuration()
        self.cfg.api_key['api-key'] = mykey.SIB_API_KEY
        self.instance = (sib.ContactsApi(sib.ApiClient(self.cfg)))
        self._get_contact()

    def _get_contact(self):
        self.error = None
        self.contact = None
        try:
            # Retrieves contact informations
            self.contact = self.instance.get_contact_info(self.email)
        except ApiException as e:
            self.error = e
