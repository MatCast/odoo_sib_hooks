# -*- coding: utf-8 -*-
{
    'name': "sib_hooks",

    'summary': """
        Webhooks to retrieve SendinBlue data""",

    'description': """
        Creates the webhooks addresses to retreive SendinBlue data.
        Handels the incoming data updating the leads in the CRM.
        Uses Send In Blue API to connect get contact information.
    """,

    'author': "Matteo Castellani. Leon Gmbh",
    'website': "http://www.leon-aperture.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Customer Relationship Management',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base'],
}
