from odoo import models, fields


class MyProjectInfo(models.Model):
    _name = 'my.project.info'
    _description = 'Information about a project'

    name = fields.Char(required=True)
    password = fields.Char()

