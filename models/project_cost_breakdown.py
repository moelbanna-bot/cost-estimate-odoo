from odoo import models,fields,api

class ProjectCostBreakdown(models.Model):
    _name = "project.cost.breakdown"
    _description = "Project Cost Breakdown Model"

    name = fields.Char("Breakdown Description" , required=True)
    estimate_id = fields.Many2one("project.cost.estimate" , "Cost Estimate" , ondelete="cascade")
    cost = fields.Float("Cost")
    quantity = fields.Float("Quantity")
    subtotal = fields.Float("Subtotal" , compute="_compute_subtotal")
    currency_id = fields.Many2one("res.currency" , "Currency")


    @api.depends("cost" , "quantity")
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.cost * rec.quantity