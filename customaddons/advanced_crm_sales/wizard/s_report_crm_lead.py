from odoo import fields, models, api, _
from datetime import date


class SReportCrmLead(models.TransientModel):
    _name = 's.report.crm.lead'

    month = fields.Selection([
        ('0', date.today().strftime('%B')),
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string='Month', default='0', required=True)
    sale_team_id = fields.Many2many('crm.team', string='Sale Team')

    # Filter data by sale_team, by selected month
    def btn_confirm(self):
        if self.month and self.sale_team_id:
            if self.month == '0':
                self.month = str(date.today().month)
            sale_teams_id = self.sale_team_id.mapped('id')
            context = {
                'name': _("Detail Report"),
                'view_mode': 'tree',
                'res_model': 'crm.lead',
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('crm.crm_case_tree_view_oppor').id,
                'target': 'current',
                'domain': [('sales_team_id', 'in', sale_teams_id), ('create_month', '=', int(self.month))],
                'context': {'create': False, 'edit': False, 'delete': False}
            }

        else:
            if self.month == '0':
                self.month = str(date.today().month)
            context = {
                'name': _("Detail Report"),
                'view_mode': 'tree',
                'res_model': 'crm.lead',
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('crm.crm_case_tree_view_oppor').id,
                'target': 'current',
                'domain': [('create_month', '=', int(self.month))],
                'context': {'create': False, 'edit': False, 'delete': False}
            }
        return context
