from odoo import models, fields, api, _


class SSaleOrder(models.Model):
    _inherit = 'sale.order'

    hide = fields.Boolean(default=True)

    def _domain_plan_sale_order_id(self):
        id_results = self.env['sale.order'].search([], order='id desc', limit=1)
        sale_order_ids = id_results.id

        quotation_results = self.env['plan.sale.order'].search(
            [('quotation', '=', sale_order_ids), ('state', 'in', ['approve', 'refuse'])])
        quotation_ids = quotation_results.mapped('id')

        return [('id', 'in', quotation_ids)]

    plan_sale_order_id = fields.Many2one('plan.sale.order', string='Plan Sale Order', domain=_domain_plan_sale_order_id)

    def create_plan_sale_order(self):
        self.hide = False
        if self.partner_id:
            return {
                'name': self.partner_id.name,
                'view_mode': 'form',
                'res_model': 'plan.sale.order',
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('advanced_crm_sales.plan_sale_order_view_form').id,
                'target': 'current',
            }

    # Override check added plan and plan approved
    def action_confirm(self):
        res = super(SSaleOrder, self).action_confirm()

        if self.plan_sale_order_id:
            if self.plan_sale_order_id.state == 'approve':
                return res
            elif self.plan_sale_order_id.state == 'refuse':
                raise models.ValidationError('The business plan has not been approved yet')
        else:
            raise models.ValidationError('The business plan has not been added')
