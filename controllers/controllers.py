# -*- coding: utf-8 -*-
from odoo import http
import logging
from . import data_handler as dh
_logger = logging.getLogger(__name__)


class ToPost(http.Controller):
    @http.route('/to_post/sib_contact_update/', type='json',
                website=True, auth="public",
                methods=['POST'], csrf=False)
    def insert_library_book(self, **kwargs):
        client = dh.Client(http.request.httprequest)
        client.update_lead()
        return 'Hey There ###: {0}'.format('ciao')
