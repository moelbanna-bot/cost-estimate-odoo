from odoo import models, fields

class SoftDeleteModel(models.AbstractModel):
    _name = "soft.delete.model"
    _description = "Abstract Model to use in other models for soft deletion"

    active = fields.Boolean("Active", default=True)

    def unlink(self):
        self.write({"active": False})
        return True
