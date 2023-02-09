# -*- coding: utf-8 -*-
{
    'name': "advanced_crm_sales",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'sale'],

    # always loaded
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/s_crm_lead.xml',
        'views/s_crm_team.xml',
        'views/plan_sale_order.xml',
        'views/s_sale_order.xml',
        'views/indicator_evaluation.xml',
        'wizard/s_report_crm_lead.xml',
        'wizard/report_indicator_evaluation.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
}
