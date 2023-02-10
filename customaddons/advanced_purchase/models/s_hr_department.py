from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SHrDepartment(models.Model):
    _inherit = 'hr.department'

    spending_limit = fields.Float(string='Spending Limit/Month')
    create_month = fields.Integer(string='Create Month', compute='_compute_create_month', store=True)
    real_cost = fields.Float(string='Real Cost', compute='_compute_real_cost')

    @api.onchange('spending_limit')
    def _onchange_spending_limit(self):
        if self.spending_limit:
            if self.spending_limit < 0:
                raise ValidationError("The expected price must be strictly positive")

    @api.depends('create_date')
    def _compute_create_month(self):
        for rec in self:
            if rec.create_date:
                rec.create_month = rec.create_date.month

    def _compute_real_cost(self):
        for rec in self:
            if rec.name:
                amount_total = self.env['purchase.order'].search([('hr_department_id', '=', rec.id)])
                amount_total_department = amount_total.mapped('amount_total')
                rec.real_cost = sum(amount_total_department)
