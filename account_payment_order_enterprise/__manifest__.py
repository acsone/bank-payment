# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Account Payment Order Enterprise',
    'summary': """
        This addon ensures the compatibility of the account_payment_order
        addon with the Odoo 12 Enterprise Accounting addon.""",
    'version': '12.0.1.0.0',
    'license': 'LGPL-3',
    'author': 'Odoo Community Association (OCA), ACSONE SA/NV',
    'website': 'https://github.com/OCA/bank-payment',
    'category': 'Banking addons',
    'depends': [
        # Odoo Enterprise
        'account_accountant',
        # OCA Bank-Payment
        'account_payment_order',
    ],
    'data': [
        'views/menus.xml',
    ],
    'auto_install': True,
}
