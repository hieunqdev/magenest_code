from odoo import models, fields, api, _


class SSaleOrder(models.Model):
    _inherit = 'sale.order'

    plan_sale_order_id = fields.Many2one('plan.sale.order', string='Plan Sale Order')

    def create_plan_sale_order(self):
        if self.partner_id:
            return {
                'name': self.partner_id.name,
                'view_mode': 'form',
                'res_model': 'plan.sale.order',
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('advanced_crm_sales.plan_sale_order_view_form').id,
                'target': 'current',
            }
