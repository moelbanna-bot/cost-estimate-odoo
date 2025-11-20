from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    cost_estimate_ids = fields.One2many(
        'project.cost.estimate',
        'project_id',
        string='Cost Estimates'
    )
    cost_estimate_count = fields.Integer(
        string='Cost Estimate Count',
        compute='_compute_cost_estimate_count'
    )
    latest_cost_estimate_id = fields.Many2one(
        'project.cost.estimate',
        string='Latest Cost Estimate',
        compute='_compute_latest_cost_estimate',
        store=True
    )
    latest_cost_estimate_total = fields.Float(
        string='Latest Total Cost',
        related='latest_cost_estimate_id.estimated_total_cost',
        store=True
    )
    latest_cost_estimate_state = fields.Selection(
        string='Latest Estimate State',
        related='latest_cost_estimate_id.state',
        store=True
    )

    @api.depends('cost_estimate_ids')
    def _compute_cost_estimate_count(self):
        for project in self:
            project.cost_estimate_count = len(project.cost_estimate_ids)

    @api.depends('cost_estimate_ids')
    def _compute_latest_cost_estimate(self):
        for project in self:
            latest_estimate = self.env['project.cost.estimate'].search([
                ('project_id', '=', project.id)
            ], order='create_date desc', limit=1)
            project.latest_cost_estimate_id = latest_estimate

    def action_view_cost_estimates(self):
        action = self.env['ir.actions.actions']._for_xml_id('project_cost_estimate.action_create_project_cost_estimate')
        view_id = self.env.ref('project_cost_estimate.project_cost_estimate_list_view').id
        action['views'] = [(view_id, 'list')]
        action['domain'] = [('project_id', '=', self.id)]
        return action

