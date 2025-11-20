from odoo import models,fields,api
from odoo.exceptions import UserError


class ProjectCostEstimate(models.Model):
    _name = "project.cost.estimate"
    _description = "Project Cost Estimate Model"
    _order = "id desc"
    _inherit = ["soft.delete.model" , "mail.thread" , "mail.activity.mixin"]

    name = fields.Char("Cost Estimate Name" , required=True)
    project_id = fields.Many2one("project.project" , "Linked Project" , required=True)
    breakdown_ids = fields.One2many("project.cost.breakdown" , "estimate_id" , "Cost Breakdowns")
    estimated_total_cost = fields.Float("Estimated Total Cost" , compute="_compute_total_cost")
    state = fields.Selection([
            ("draft" , "Draft"),
            ("submitted" , "Submitted"),
            ("approved" , "Approved"),
            ("rejected" , "Rejected"),
        ] , default="draft" , tracking=True)

    created_by = fields.Many2one("res.users" , "Created By" , default=lambda self: self.env.user.id)
    @api.depends("breakdown_ids.subtotal")
    def _compute_total_cost(self):
        for rec in self:
            # total = 0.0
            # for breakdown in rec.breakdown_ids:
            #     total += breakdown.subtotal
            # rec.estimated_total_cost = total
            rec.estimated_total_cost = sum(rec.breakdown_ids.mapped('subtotal'))

    def _is_allowed_state_transition(self,old_state,new_state):
        allowed = [
            ("draft","submitted"),
            ("submitted","approved"),
            ("submitted","rejected"),
            ("rejected","draft")
        ]
        return (old_state,new_state) in allowed

    def change_state(self,new_state):
        for rec in self:
            # print(f" record state : {rec.state}")
            if not rec._is_allowed_state_transition(rec.state,new_state):
                raise UserError(f"Can't transition from {rec.state} to {new_state}")
        return self.write({"state":new_state})

    def write(self, vals):
        if 'state' in vals:
            new_state = vals['state']
            for rec in self:
                if rec.state != new_state:
                    if not rec._is_allowed_state_transition(rec.state, new_state):
                        raise UserError(f"Can't transition from {rec.state} to {new_state}")

        if 'state' in vals and vals['state'] == 'approved':
            if not self.env.user.has_group('project_cost_estimate.project_cost_estimate_group_approver'):
                raise UserError('You do not have permission to change the stete to Approved.')

        return super(ProjectCostEstimate, self).write(vals)

    def action_submit(self):
        # print("Submitting Cost Estimate...")
        self.change_state("submitted")

    def action_approve(self):
        self.send_mail('approved')
        self.write({"state":"approved"})

    def action_reject(self):
        self.send_mail('rejected')
        self.change_state("rejected")

    def action_set_to_draft(self):
        self.change_state("draft")

    def send_mail(self,state):
        if state == 'approved':
            self.message_post_with_source('project_cost_estimate.mail_template_cost_estimate_approved')
        elif state == 'rejected':
            self.message_post_with_source('project_cost_estimate.mail_template_cost_estimate_rejected')