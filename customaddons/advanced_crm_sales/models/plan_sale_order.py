from odoo import models, fields, api
from odoo.exceptions import UserError


class PlanSaleOrder(models.Model):
    _name = 'plan.sale.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Text(string="Name", required=True)
    quotation = fields.Many2one('sale.order', string='Quotation')
    content = fields.Text(string='Content', required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('send', 'Send'),
        ('approve', 'Approve'),
        ('refuse', 'Refuse'),
    ], string='State', default='new')
    approver_id = fields.One2many('approver.list', 'plan_sale_order_id', string='Approver')
    hide = fields.Boolean(string='Hide', compute="_compute_hide")

    def _compute_hide(self):
        current_uid = self.env.uid
        for rec in self:
            if rec.create_uid:
                if rec.create_uid.id != current_uid:
                    rec.hide = True
                else:
                    rec.hide = False

    def btn_send(self):
        if self.state == 'new':
            if self.approver_id:
                self.state = 'send'
                self.message_post(partner_ids=self.approver_id.approver.mapped('id'),
                                  body='The new plan has been sent.')
            else:
                raise UserError('Please write your approvers')
        else:
            raise UserError('Cannot confirm this approve')
