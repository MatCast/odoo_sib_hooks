# -*- coding: utf-8 -*-
import yaml
import logging

_logger = logging.getLogger(__name__)

SIB_MAP_TXT = {
    'email': 'partner_address_email',
    'sms': 'phone',
    'azienda': 'partner_name',
    'nome_e_cognome': 'street',
    'indirizzo': 'street2',
    'cap': 'zip',
    'localita': 'city',
    'odoo_id': 'id'
    }

SIB_MAP_DB = {
    'provincia': {'res.country.state': 'state_id'},
    'utm_source': {'utm.source': 'source_id'},
    'utm_campaign': {'utm.campaign': 'campaign_id'},
    'utm_medium': {'utm.medium': 'medium_id'},
}
"""
COGNOME
NOME
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
        self.data = self._parse_data()
        self.headers = response.headers

    def _parse_data(self):
        try:
            data_json = yaml.load(self.response.data)
        except yaml.YAMLError as e:
            _logger.info(e)
            data_json = {}
        return data_json

    def _map_data(self):
        if self.data:
