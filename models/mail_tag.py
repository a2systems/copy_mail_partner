##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MailCommunicationTag(models.Model):
    _name = 'mail.communication.tag'
    _description = 'mail.communication.tag'

    name = fields.Char('Name')
    active = fields.Boolean('Active',default=True)
