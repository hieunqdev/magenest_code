from odoo import models, fields, api
from datetime import date


class SIndicatorEvaluation(models.Model):
    _inherit = 'indicator.evaluation'

    real_revenue_difference = fields.Float(string='Real Revenue Difference', compute='_compute_real_revenue_difference')

    def _compute_real_revenue_difference(self):
        current_month = date.today().month

        for rec in self:
            if rec.real_revenue:
                month_sales_result = self.env['crm.team'].search([('id', 'in', rec.sale_team_id.mapped('id'))])
                month_sales = month_sales_result.mapped(lambda res: (res.january_sales, res.february_sales,
                                                                     res.march_sales, res.april_sales, res.may_sales,
                                                                     res.june_sales, res.july_sales, res.august_sales,
                                                                     res.september_sales, res.october_sales,
                                                                     res.november_sales, res.december_sales))

                rec.real_revenue_difference = rec.real_revenue - month_sales[0][current_month - 1]
            else:
                rec.real_revenue_difference = 0.00
