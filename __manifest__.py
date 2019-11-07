# -*- coding: utf-8 -*-
{
    'name': "sib_hooks",

    'summary': """
        Webhooks to retrieve SendinBlue data""",

    'description': """
        Creates the webhooks addresses to retreive SendinBlue data.
        Handels the incoming data updating the leads in the CRM
    """,

    'author': "Matteo Castellani. Leon Gmbh",
    'website': "http://www.leon-aperture.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Customer Relationship Management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}