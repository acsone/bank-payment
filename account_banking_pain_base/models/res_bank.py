# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from odoo import api, models, _
from odoo.exceptions import ValidationError


class ResBank(models.Model):
    _inherit = 'res.bank'

    @api.multi
    @api.constrains('bic')
    def _check_bic(self):
        """
        This method strengthens the constraint on the BIC of the bank account
        (The account_payment_order module already checks the length in the
         check_bic_length method).
        :raise: ValidationError if the BIC doesn't respect the regex of the
        SEPA pain schemas.
        """
        bic_re = r"[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}"
        invalid_banks = self.filtered(lambda r: not re.match(bic_re, r.bic))
        if invalid_banks:
            raise ValidationError(_(
                "The following Bank Identifier Codes (BIC) does not respect "
                "the SEPA pattern:\n{bic_list}\n\nSEPA pattern: "
                "{sepa_pattern}").format(
                sepa_pattern=bic_re,
                bic_list="\n".join(invalid_banks.mapped('bic'))
            ))
