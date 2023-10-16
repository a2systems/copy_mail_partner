# -*- coding: utf-8 -*-
{
    'name': 'copy_mail_partner',
    'version': '14.0.1',
    'category': 'Social',
    'depends': [
               'mail',
               'base',
                ],
    'data':[
       'views/partner.xml',
       'views/tag.xml',
       'views/template.xml',
       'security/ir.model.access.csv'
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
