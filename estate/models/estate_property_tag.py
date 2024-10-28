from odoo import fields, models


class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _order = 'name'

    name = fields.Char(required=True)

    _sql_constraints = [('unique_tag', 'UNIQUE (name)', 'Tag name must be unique')]

    color = fields.Integer()