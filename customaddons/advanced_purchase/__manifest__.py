# -*- coding: utf-8 -*-
{
    'name': "advanced_purchase",

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
    'depends': ['base', 'hr', 'purchase'],

    # always loaded
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/s_hr_department.xml',
        'views/s_purchase_order.xml',
        'views/order_limit.xml',
        'views/employee_order_limit.xml',
        'wizard/s_choice_department.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/s_hr_department_demo_data.xml',
    ],
}
