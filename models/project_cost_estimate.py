from odoo import models,fields,api


class ProjectCostEstimate(models.Model):
    _name = "project.cost.estimate"
    _description = "Project Cost Estimate Model"
    _order = "id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char("Cost Estimate Name" , required=True)
    project_id = fields.Many2one("project.project" , "Linked Project" , required=True)
    breakdown_ids = fields.One2many("project.cost.breakdown" , "estimate_id" , "Cost Breakdowns")
    estimated_total_cost = fields.Float("Estimated Total Cost" , compute="_compute_total_cost")


    @api.depends("breakdown_ids.subtotal")
    def _compute_total_cost(self):
        for rec in self:
            # total = 0.0
            # for breakdown in rec.breakdown_ids:
            #     total += breakdown.subtotal
            # rec.estimated_total_cost = total
            rec.estimated_total_cost = sum(rec.breakdown_ids.mapped('subtotal'))