from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    _sql_constraints = [('unique_type', 'UNIQUE (name)', 'Type name must be unique')]

    property_ids = fields.One2many('estate.property', 'type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    sequence = fields.Integer('Sequence')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
