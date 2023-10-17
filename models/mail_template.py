##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import _, api, fields, models, tools, Command
from odoo.exceptions import ValidationError
from odoo.tools import is_html_empty


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    def generate_recipients(self, results, res_ids):
        self.ensure_one()
        results = super(MailTemplate, self).generate_recipients(results, res_ids)
        if type(results) == dict:
            for key, values in results.items():
                if type(values) == dict:
                    for other_key,other_values in values.items():
                        if other_key == 'partner_ids':
                            partner_ids = other_values
                            for partner_id in partner_ids:
                                tag_ids = self.mail_tag_ids.ids
                                child_partners = self.env['res.partner'].search([('parent_id','=',partner_id)])
                                for child_partner in child_partners:
                                    for child_tag in child_partner.mail_tag_ids.ids:
                                        if child_tag in tag_ids and child_partner.id not in partner_ids:
                                            partner_ids.append(child_partner.id)
                                results[key]['partner_ids'] = partner_ids
        return results

    def x_generate_recipients(self, results, res_ids):
        """Generates the recipients of the template. Default values can ben generated
        instead of the template values if requested by template or context.
        Emails (email_to, email_cc) can be transformed into partners if requested
        in the context. """
        self.ensure_one()

        if self.use_default_to or self._context.get('tpl_force_default_to'):
            records = self.env[self.model].browse(res_ids).sudo()
            default_recipients = records._message_get_default_recipients()
            for res_id, recipients in default_recipients.items():
                results[res_id].pop('partner_to', None)
                results[res_id].update(recipients)

        records_company = None
        if self._context.get('tpl_partners_only') and self.model and results and 'company_id' in self.env[self.model]._fields:
            records = self.env[self.model].browse(results.keys()).read(['company_id'])
            records_company = {rec['id']: (rec['company_id'][0] if rec['company_id'] else None) for rec in records}

        for res_id, values in results.items():
            partner_ids = values.get('partner_ids', list())
            if self._context.get('tpl_partners_only'):
                mails = tools.email_split(values.pop('email_to', '')) + tools.email_split(values.pop('email_cc', ''))
                Partner = self.env['res.partner']
                if records_company:
                    Partner = Partner.with_context(default_company_id=records_company[res_id])
                for mail in mails:
                    partner = Partner.find_or_create(mail)
                    partner_ids.append(partner.id)
            partner_to = values.pop('partner_to', '')
            if partner_to:
                # placeholders could generate '', 3, 2 due to some empty field values
                tpl_partner_ids = [int(pid.strip()) for pid in partner_to.split(',') if (pid and pid.strip().isdigit())]
                partner_ids += self.env['res.partner'].sudo().browse(tpl_partner_ids).exists().ids
            for partner_id in partner_ids:
                tag_ids = self.mail_tag_ids.ids
                child_partners = self.env['res.partner'].search([('parent_id','=',partner_id)])
                for child_partner in child_partners:
                    for child_tag in child_partner.mail_tag_ids.ids:
                        if child_tag in tag_ids and child_partner.id not in partner_ids:
                            partner_ids.append(child_partner.id)
            results[res_id]['partner_ids'] = partner_ids
        return results

    mail_tag_ids = fields.Many2many(comodel_name='mail.communication.tag',relname='template_tag_rel',col1='template_id',col2='tag_id',string='Mail Tags')
