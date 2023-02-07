from odoo import models, fields


class AprroverList(models.Model):
    _name = 'approver.list'

    approver = fields.Many2one('res.partner', string='Approver')
    approval_status = fields.Selection([
        ('not approved yet', 'Not Approved Yet'),
        ('approve', 'Approve'),
        ('refuse', 'Refuse'),
    ], default='not approved yet', string='Status', readonly=True)
    plan_sale_order_id = fields.Many2one('plan.sale.order', string='Plan Sale Order', readonly=True)

    def btn_approve(self):
        self.approval_status = 'approve'
        states = self.plan_sale_order_id.approver_id.mapped('approval_status')
        if all([state == 'approve' for state in states]):
            self.plan_sale_order_id.state = 'approve'

    def btn_refuse(self):
        self.approval_status = 'refuse'
        states = self.plan_sale_order_id.approver_id.mapped('approval_status')
        if all([state == 'refuse' for state in states]):
            self.plan_sale_order_id.state = 'refuse'
