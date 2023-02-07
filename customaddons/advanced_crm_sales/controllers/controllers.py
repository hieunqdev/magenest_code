# -*- coding: utf-8 -*-
# from odoo import http


# class AdvancedCrmSales(http.Controller):
#     @http.route('/advanced_crm_sales/advanced_crm_sales', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/advanced_crm_sales/advanced_crm_sales/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('advanced_crm_sales.listing', {
#             'root': '/advanced_crm_sales/advanced_crm_sales',
#             'objects': http.request.env['advanced_crm_sales.advanced_crm_sales'].search([]),
#         })

#     @http.route('/advanced_crm_sales/advanced_crm_sales/objects/<model("advanced_crm_sales.advanced_crm_sales"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('advanced_crm_sales.object', {
#             'object': obj
#         })
