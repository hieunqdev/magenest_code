from odoo import http
from odoo.http import request
import json


class SalesPurchase(http.Controller):
    @http.route('/api-report', type='http', auth='none', methods=["POST"], csrf=False)
    def sales_purchase(self, **kwargs):
        body = json.loads(request.httprequest.data)
        access_token = "odooneverdie"

        if body["token"] == access_token and body["month"]:
            indicator_evaluation = request.env['indicator.evaluation'].sudo().search([('month', '=', body["month"])])
            hr_department = request.env['hr.department'].sudo().search([('create_month', '=', body["month"])])

            context = {
                "sales": [],
                "purchase": []
            }

            for indicator in indicator_evaluation:
                context["sales"].append({
                    "sale_team_name": indicator.sale_team_id.name,
                    "real_revenue": indicator.real_revenue,
                    "diff": indicator.real_revenue_difference
                })

            for department in hr_department:
                context["purchase"].append({
                    "department_name": department.name,
                    "real_cost": department.real_cost,
                    "diff": department.real_cost_difference
                })

        else:
            context = {
                "status": "The service is temporarily unavailable",
                "content": "The service in charge of the requested endpoint is temporarily unavailable or unreachable."
            }

        json_context = json.dumps(context, indent=4)
        return json_context
