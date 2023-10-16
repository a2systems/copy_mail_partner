##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.model_create_multi
    def create(self, values_list):
        new_mails = super(MailMail, self).create(values_list)
        for new_mail in new_mails:
            partners = new_mail.partner_ids.ids
            for partner in new_mail.partner_ids:
                child_partners = self.env['res.partner'].search([('parent_id','=',partner.id),('copy_mail_from_parent','=',True)])
                for child_partner in child_partners:
                    partners.append(child_partner.id)
            new_mail.partner_ids = [(6,0,partners)]
            new_mail.recipient_ids = [(6,0,partners)]
        return new_mails

