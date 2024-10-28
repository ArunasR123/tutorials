from odoo import api, fields, models, exceptions, tools


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Datetime.add(fields.Datetime.today(), months=3), copy=False)

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)

    _sql_constraints = [
        ('check_strictly_positive', 'CHECK (expected_price > 0)', 'Expected price must be strictly positive'),
        ('check_positive', 'CHECK (selling_price >= 0)', 'Selling price must be strictly positive')]

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])

    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
         ('cancelled', 'Cancelled')], required=True, copy=False, default='new')

    type_id = fields.Many2one("estate.property.type")

    buyer = fields.Many2one('res.partner', copy=False)
    salesperson = fields.Many2one('res.users', default=lambda self: self.env.user)

    tag_ids = fields.Many2many("estate.property.tag", string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    total_area = fields.Integer(compute='_compute_total')
    best_offer = fields.Float(compute='_compute_best_offer')

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_not_new_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise exceptions.UserError('Cannot delete this property')

    @api.depends('garden_area', 'living_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if self.offer_ids:
                record.best_offer = max(self.offer_ids.mapped('price'))
            else:
                record.best_offer = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def property_sold(self):
        for record in self:
            if record.state != 'cancelled' and record.state != 'sold':
                record.state = 'sold'
            else:
                raise exceptions.UserError('Property can not be marked as Sold')
        return True

    def property_cancelled(self):
        for record in self:
            if record.state != 'cancelled' and record.state != 'sold':
                record.state = 'cancelled'
            else:
                raise exceptions.UserError('Property can not be marked as Cancelled')
        return True

    @api.constrains('expected_price', 'selling_price')
    def _check_expected_price(self):
        for record in self:
            if tools.float_compare(record.selling_price * 0.9, record.expected_price,
                                   precision_digits=3) < 0 and not tools.float_is_zero(record.selling_price,
                                                                                       precision_digits=3):
                raise exceptions.ValidationError('Selling price must be at least 90% of the expected price.')
