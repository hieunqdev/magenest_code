from odoo import models, fields, api


class SPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    vendor = fields.Char(string='Supplier')

    @api.onchange('product_id')
    def _onchange_vendor(self):
        if self.product_id:
            vendor_line_price = self.env['product.supplierinfo'].search([('product_id', '=', self.product_id.id)], order='price asc')
            vendor_line = vendor_line_price.mapped(lambda res: (res.price, res.delay, res.partner_id.name))
            vendor_line.sort()
            if vendor_line:
                self.vendor = vendor_line[0][2]
            else:
                self.vendor = ''
