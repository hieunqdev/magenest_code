from odoo import models, fields, api


class SPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    vendor = fields.Char(string='Supplier')

    # Check supplier for cheapest price
    # Check supplier for shortest delivery time
    @api.onchange('product_id')
    def _onchange_vendor(self):
        if self.product_id:
            vendor_line_price = self.env['product.supplierinfo'].search([('product_id', '=', self.product_id.id)],
                                                                        order='price asc')
            vendor_price = vendor_line_price.mapped('price')

            if len(vendor_price) == 1:
                self.vendor = vendor_line_price.partner_id.name
            else:
                vendor_line_delay = self.env['product.supplierinfo'].search(
                    [('product_id', '=', self.product_id.id), ('price', 'in', vendor_price)], order='delay asc',
                    limit=1)
                self.vendor = vendor_line_delay.partner_id.name
