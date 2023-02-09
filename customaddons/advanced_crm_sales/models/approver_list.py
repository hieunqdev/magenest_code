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
    hide = fields.Boolean(string='Hide', compute="_compute_hide")

    def btn_approve(self):
        self.approval_status = 'approve'
        self.plan_sale_order_id.message_post(partner_ids=self.plan_sale_order_id.create_uid.mapped('id'),
                                             body='Responded')
        states = self.plan_sale_order_id.approver_id.mapped('approval_status')
        if all([state == 'approve' for state in states]):
            self.plan_sale_order_id.state = 'approve'

    def btn_refuse(self):
        self.approval_status = 'refuse'
        self.plan_sale_order_id.message_post(partner_ids=self.plan_sale_order_id.create_uid.mapped('id'),
                                             body='Responded')
        self.plan_sale_order_id.state = 'refuse'

    def _compute_hide(self):
        current_uid = self.env.uid
        partner_id_results = self.env['res.users'].search([('id', '=', current_uid)])
        partner_id = partner_id_results.partner_id.id

        for rec in self:
            if rec.approver:
                if rec.approver.id != partner_id:
                    rec.hide = True
                else:
                    rec.hide = False
