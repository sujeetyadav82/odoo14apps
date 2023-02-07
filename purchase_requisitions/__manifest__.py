# -*- coding: utf-8 -*-
{
    'name': "purchase_requisitions",

    'summary': """
           Product/Material Purchase Requisitions by Employees/Users""",

    'description': """
        Long description of module's purpose
    """,
    'sequence':-101,
    'author': "Redian Software",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','purchase'],

    # always loaded
    'data': ['security/Purchase_req_security.xml',
        'security/ir.model.access.csv',
        'data/purchase.xml',
         'views/commission_shift.xml',

             'report/report.xml',
             'report/report_template.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images':['static/description/3718757@0.jpg'],
}
