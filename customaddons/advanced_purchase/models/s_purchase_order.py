from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    hr_department_id = fields.Many2one('hr.department', string='Department', required=True)

    # Override check the creator has exceeded the limit
    def button_confirm(self):
        current_uid = self.env.uid
        accountant_ids = self.env.ref('advanced_purchase.group_staff_accountant').users.ids

        employee_line = self.env['employee.order.limit'].search([('employee_id', '=', current_uid)], limit=1)
        order_limit_employee = employee_line.order_limit

        if self.amount_total:
            if (self.amount_total < order_limit_employee) or (current_uid in accountant_ids):
                self.message_post(body='Purchase Order created')
                return super(SPurchaseOrder, self).button_confirm()
            else:
                raise ValidationError('The total request exceeds the limit. Please send it to the accountant.')
