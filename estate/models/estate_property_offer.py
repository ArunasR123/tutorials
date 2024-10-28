from odoo import fields, models, api, exceptions
from odoo.api import ValuesType, Self


class EstatePropertyOffers(models.Model):
    _name = "estate.property.offer"
    _order = 'price desc'

    price = fields.Float()

    _sql_constraints = [('check_strictly_positive', 'CHECK (price > 0)', 'offer price must be strictly positive')]

    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_compute_deadline_inverse')

    property_type_id = fields.Many2one('estate.property.type', related='property_id.type_id', store=True)

    @api.model
    def create(self, vals_list):
        property = self.env['estate.property'].browse(vals_list['property_id']);

        if any(offer.price > vals_list['price'] for offer in property.offer_ids):
            raise exceptions.UserError('Your offer price can not be lower that the highest bid.')
        property.state = 'offer_received'
        return super().create(vals_list)

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            if record.get_metadata()[0]['create_date']:
                record.date_deadline = fields.Date.add(record.get_metadata()[0]['create_date'], days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _compute_deadline_inverse(self):
        for record in self:
            record.validity = (record.date_deadline - record.get_metadata()[0]['create_date'].date()).days

    def accept_offer(self):
        for record in self:
            for offer_on_property in record.property_id.offer_ids:
                if offer_on_property == record:
                    continue
                if offer_on_property.status == 'accepted':
                    raise exceptions.UserError('Only one offer per property can be accepted')
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            record.status = 'accepted'
        return True

    def refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
