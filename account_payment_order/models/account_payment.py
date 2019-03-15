# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def _compute_journal_domain_and_types(self):
        res = super(AccountPayment, self)._compute_journal_domain_and_types()
        journal_domain = res.get('domain', [])
        if self.payment_type == 'inbound':
            journal_domain.append(('inbound_payment_order_only', '=', False))
        else:
            journal_domain.append(('outbound_payment_order_only', '=', False))
        res['domain'] = journal_domain
        return res
