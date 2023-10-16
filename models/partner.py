##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    mail_tag_ids = fields.Many2many(comodel_name='mail.communication.tag',relname='partner_tag_rel',col1='partner_id',col2='tag_id',string='Mail Tags')
