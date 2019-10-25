# -*- coding: utf-8 -*-
from odoo import http
import logging
import data_handler as dh
_logger = logging.getLogger(__name__)



class ToPost(http.Controller):
    @http.route('/to_post/to_post/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/to_post/post_here/', type='json',
                website=True, auth="public",
                methods=['POST'], csrf=False)
    def insert_library_book(self, **kwargs):
        # record = request.env['library.book']
        # record.create(kwargs)
        data = http.request.httprequest.data
        headers = http.request.httprequest.headers
        data_in_json = yaml.load(data)
        records = http.request.env['crm.lead'].sudo().search([])
        records[0].write({'source_id': 'Facebook'})
        _logger.info('HERE LOGGING{0}!!!!!!!!!!!!'.format(records))
        return 'Hey There ###: <br>{0}'.format(records[0].name)
