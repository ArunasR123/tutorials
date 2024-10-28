from odoo import fields, models


class PropertyUsers(models.Model):
    # _name = 'property.users'
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'salesperson', domain="['|',('state','=', 'new'),('state','=','offer_received')]")
