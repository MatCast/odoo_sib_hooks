# -*- coding: utf-8 -*-
import yaml
import logging
from odoo.http import request
from . import sib_api_handler as sibh

_logger = logging.getLogger(__name__)

SIB_MAP_TXT = {
    'email': 'email_from',
    'sms': 'phone',
    'azienda': 'partner_name',
    'nome_e_cognome': 'street',
    'indirizzo': 'street2',
    'cap': 'zip',
    'localita': 'city',
    'odoo_id': 'id',
    'email_count': 'x_email_count',
    'score': 'x_score'
    }

SIB_MAP_DB = {
    'provincia': 'res.country.state',
    'utm_source': 'utm.source',
    'utm_campaign': 'utm.campaign',
    'utm_medium': 'utm.medium',
}

MODEL_ID = {
    'res.country.state': 'state_id',
    'utm.source': 'source_id',
    'utm.campaign': 'campaign_id',
    'utm.medium': 'medium_id',
}
"""
DOUBLE_OPT-IN
PRIVACY
UTM_TERM
UTM_CONTENT
VIES
PARTITA_IVA
EMAIL_COUNT
"""


class Client(object):
    def __init__(self, response):
        self.response = response
        self.data_json = self._parse_data()
        self.data = self._data_attributes()
        self.headers = response.headers
        self.record = None
        self.user_agent = False
        self._check_user_agent()
        self._map_data()
        self._parse_name()
        self.email = self._get_email()
        self.contact = self._get_sib_contact()
        self.odoo_id = self._get_odoo_id()

    def _parse_data(self):
        try:
            data_json = yaml.load(self.response.data)
        except yaml.YAMLError as e:
            _logger.info(e)
            data_json = {}
        return data_json

    def _data_attributes(self):
        attr = self.data_json['content'][0]['attributes']
        return dict((k.lower(), v) for k, v in attr.items())

    def _get_email(self):
        content = self.data_json.get('content')
        if content:
            return content[0].get('email')

    def _get_sib_contact(self):
        sibc = sibh.SibContact(self.email)
        if sibc.error:
            to_log = "Exception when calling ContactsApi->get_contact_info: {}"
            _logger.info(to_log.format(sibc.error))
        return sibc.contact

    def _get_odoo_id(self):
        id_odoo = None
        if self.contact and 'ODOO_ID' in self.contact.attributes.keys():
            id_odoo = self.contact.attributes.get('ODOO_ID')
            self.txt_map.pop('id', None)
        elif 'id' in self.txt_map.keys():
            id_odoo = self.txt_map.get('id')
            self.txt_map.pop('id', None)
        return id_odoo

    def _map_data(self):
        # looks like {'partner_address_email' : 'example@email.com'}
        self.txt_map = {}
        # looks like {'res.country.state' : 'Vercelli'}
        self.db_map = {}
        # looks like self.data = {'email': 'example@email.com'}
        for key in self.data:
            if key in SIB_MAP_TXT.keys():
                # looks like SIB_MAP_TXT = {'email': 'partner_address_email'}
                self.txt_map[SIB_MAP_TXT[key]] = self.data[key]
            elif key in SIB_MAP_DB.keys():
                # looks like SIB_MAP_DB = {'provincia': 'res.country.state'}
                self.db_map[SIB_MAP_DB[key]] = self.data[key]

    def _parse_name(self):
        """Put together name and surname."""
        k = self.data.keys()
        name = ''
        surname = ''
        if 'cognome' in k:
            surname = self.data['cognome']
        if 'nome' in k:
            name = self.data['nome']
        if name or surname:
            self.txt_map['contact_name'] = (name + ' '
                                            + surname)
            self.txt_map['contact_name'] = self.txt_map['contact_name'].strip()

    def _find_record(self):
        if self.odoo_id:
            lead_id = self.odoo_id
            records = request.env['crm.lead'].sudo().search([('id',
                                                              '=',
                                                              lead_id)])
            if records:
                return records[0]

    def _handle_txt(self):
        record = self._find_record()
        if record:
            record.write(self.txt_map)
            self.record = record

    def _serach_db(self):
        # looks like {'state_id' : 23}
        to_write = {}
        for key in self.db_map:
            records = request.env[key].sudo().search([('name',
                                                       '=ilike',
                                                       self.db_map[key])])
            if len(records) == 1:
                to_write[MODEL_ID[key]] = records[0].id
            if not records:
                # no new state (provincia) should be created
                if key != 'res.country.state':
                    rec = request.env[key].create({'name': self.db_map[key]})
                    to_write[MODEL_ID[key]] = rec.id
        return to_write

    def _handle_db(self):
        record = self._find_record()
        to_write = self._serach_db()
        if record:
            record.write(to_write)
            self.record = record

    def _check_user_agent(self):
        if (self.headers.get('user-agent').lower()
                == 'SendinBlue Webhook'.lower()):
            self.user_agent = True

    def update_lead(self):
        if self.user_agent:
            self._handle_txt()
            self._handle_db()
