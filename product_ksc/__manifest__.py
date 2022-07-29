# -*- coding: utf-8 -*-
{
    'name': "product_ksc",

    'summary': """
        This is the module for products.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Sujeet",
    "sequence": -100,

    'website': "redian.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.1',
     "license": "AGPL-3",
    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
        'views/views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    "installable": True,
    'application': True
}
