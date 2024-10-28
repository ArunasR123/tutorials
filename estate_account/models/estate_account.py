from odoo import fields, models, Command


class EstateAccount(models.Model):
    _inherit = 'estate.property'

    def property_sold(self):
        values_list = []
        for record in self:
            print(record.buyer)
            values = {'move_type': 'out_invoice', 'partner_id': record.buyer.id, 'invoice_line_ids': [
                Command.create(
                    {
                        'name': 'Downpayment',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.09
                    }),
                Command.create(
                    {
                        'name': 'Administrative fee',
                        'quantity': 1,
                        'price_unit': 100.0
                    },

                )
            ]}
            values_list.append(values)

            record.check_access('create')

            self.sudo().env['account.move'].create(values_list)
        return super().property_sold()
