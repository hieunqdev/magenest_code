from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SCrmTeam(models.Model):
    _inherit = 'crm.team'

    january_sales = fields.Float(string="January Sales")
    february_sales = fields.Float(string="February Sales")
    march_sales = fields.Float(string="March Sales")
    april_sales = fields.Float(string="April Sales")
    may_sales = fields.Float(string="May Sales")
    june_sales = fields.Float(string="June Sales")
    july_sales = fields.Float(string="July Sales")
    august_sales = fields.Float(string="August Sales")
    september_sales = fields.Float(string="September Sales")
    october_sales = fields.Float(string="October Sales")
    november_sales = fields.Float(string="November Sales")
    december_sales = fields.Float(string="December Sales")

    @api.onchange('january_sales', 'february_sales', 'march_sales', 'april_sales', 'may_sales', 'june_sales',
                  'july_sales', 'august_sales', 'september_sales', 'october_sales', 'november_sales',
                  'december_sales')
    def _onchange_month_sales(self):
        if (self.january_sales < 0 or self.february_sales < 0 or self.march_sales < 0 or self.april_sales < 0
                or self.may_sales < 0 or self.june_sales < 0 or self.july_sales < 0 or self.august_sales < 0
                or self.september_sales < 0 or self.october_sales < 0 or self.november_sales < 0 or self.december_sales < 0):
            raise ValidationError("The expected price must be strictly positive")
