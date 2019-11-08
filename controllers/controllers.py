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
        client = dh.Client(http.request.httprequest)
        if client.user_agent:
            client.update_lead()
            result = 'No lead Updated'
            if client.record:
                result = 'Lead {0} Updated. ID: {1}'.format(client.record.name,
                                                            client.record.id)
        else:
            result = 'Invalid User Agent'
        return result
