from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SCrmLead(models.Model):
    _inherit = 'crm.lead'

    is_lost = fields.Boolean()
    sales_team_id = fields.Many2one('crm.team', string='Sales Team', compute='_sales_team_id')
    quotation_count = fields.Integer()
    minimum_revenue = fields.Float(string='Minimum Revenue (VAT)')

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

        if current_uid == leader_id:
            employee_ids = team_user_ids
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
