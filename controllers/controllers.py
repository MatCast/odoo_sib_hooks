# -*- coding: utf-8 -*-
from odoo import http
import logging
from . import data_handler as dh
_logger = logging.getLogger(__name__)


class ToPost(http.Controller):
    @http.route('/to_post/sib_contact_update/', type='json',
                website=True, auth="public",
                methods=['GET', 'POST'], csrf=False)
    def insert_library_book(self, **kwargs):
        _logger.info('### SIB POSTING START ###')
        string_200 = 'SIB Lead {0} Updated. ID: {1}'
        client = dh.Client(http.request.httprequest)
        if client.user_agent:
            client.update_lead()
            result = 'No lead Updated'
            if client.record:
                result = string_200.format(client.record.name,
                                           client.record.id)
                _logger.info(string_200.format(client.record.name,
                                               client.record.id))
        else:
            result = 'Invalid User Agent'
            _logger.info('SIB Invalid User Agent')
        _logger.info('### SIB POSTING END ###')
        return result
