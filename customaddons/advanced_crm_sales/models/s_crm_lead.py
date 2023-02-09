from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SCrmLead(models.Model):
    _inherit = 'crm.lead'

    is_lost = fields.Boolean()
    sales_team_id = fields.Many2one('crm.team', string='Sales Team', compute='_sales_team_id', store=True)
    quotation_count = fields.Integer()
    minimum_revenue = fields.Float(string='Minimum Revenue (VAT)')
    create_month = fields.Integer(string='Create Month', compute='_compute_create_month', store=True)
    real_revenue = fields.Float(string='Real Revenue', compute='_compute_real_revenue')

    # Only leader has the right to lose 3 stars
    def action_set_lost(self, **additional_values):
        res = super(SCrmLead, self).action_set_lost(**additional_values)

        current_uid = self.env.uid
        leader_ids = self.env.ref('advanced_crm_sales.group_staff_leader').users.ids

        if (current_uid not in leader_ids) and (self.priority == '3'):
            raise ValidationError('Only leader has the right to lose 3 stars.')

        self.is_lost = True
        return res

    def toggle_active(self):
        res = super(SCrmLead, self).toggle_active()
        self.is_lost = False
        return res

    # Only assign opportunities to yourself or sales staff. Manager can sign for everyone
    def _domain_user_id(self):
        current_uid = self.env.uid
        employee_ids = []

        crm_team_id_results = self.env['crm.team.member'].search([('user_id', '=', current_uid)])
        crm_team_ids = crm_team_id_results.crm_team_id.id

        user_id_results = self.env['crm.team.member'].search([('crm_team_id', '=', crm_team_ids)])
        team_user_ids = user_id_results.user_id.mapped('id')

        leader_id_results = self.env['crm.team'].search([('user_id', 'in', team_user_ids)])
        leader_id = leader_id_results.user_id.id

        user_ids = self.env['res.users'].search([])

        if current_uid == leader_id:
            employee_ids = user_ids.mapped('id')
        else:
            for id in team_user_ids:
                if id != leader_id:
                    employee_ids.append(id)

        return [('id', 'in', employee_ids)]

    user_id = fields.Many2one(domain=_domain_user_id)

    @api.depends('user_id')
    def _sales_team_id(self):
        for rec in self:
            if rec.user_id:
                crm_team_id_results = rec.env['crm.team.member'].search([('user_id', '=', rec.user_id.id)])
                rec.sales_team_id = crm_team_id_results.crm_team_id.id

    @api.depends('create_date')
    def _compute_create_month(self):
        for rec in self:
            if rec.create_date:
                rec.create_month = rec.create_date.month

    # Calculate real_revenue = amount_total corresponding to the opportunity
    def _compute_real_revenue(self):
        for rec in self:
            if rec.id:
                amount_total = self.env['sale.order'].search([('opportunity_id', '=', rec.id)])
                amount_total_opportunity = amount_total.mapped('amount_total')
                rec.real_revenue = sum(amount_total_opportunity)
