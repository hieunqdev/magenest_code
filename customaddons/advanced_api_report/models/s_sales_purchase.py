from odoo import models, fields, api


class SSalesPurchase(models.Model):
    _name = 's.sales.purchase'

    def btn_send_email(self):
        accountant_ids = self.env.ref('advanced_purchase.group_staff_accountant').users.ids
        res_users = self.env['res.users'].sudo().search([('id', 'in', accountant_ids)])
        email_accountant = res_users.partner_id.mapped('email')

        indicator_evaluation = self.env['indicator.evaluation'].search([])
        hr_department = self.env['hr.department'].search([])

        ctx = {}
        ctx['sale_team_name'] = indicator_evaluation.mapped('sale_team_id.name')
        ctx['real_revenue'] = indicator_evaluation.mapped('real_revenue')
        ctx['real_revenue_difference'] = indicator_evaluation.mapped('real_revenue_difference')
        ctx['department_name'] = hr_department.mapped('name')
        ctx['real_cost'] = hr_department.mapped('real_cost')
        ctx['real_cost_difference'] = hr_department.mapped('real_cost_difference')
        ctx['email_to'] = ';'.join(map(lambda x: x, email_accountant))
        ctx['email_from'] = 'laravel.ecommerce.v1@gmail.com'
        template = self.env.ref('advanced_api_report.email_template')
        template.with_context(ctx).send_mail(self.id, force_send=True, raise_exception=False)
