# Copyright 2024 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"

    filename_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        help="Sequence used to generate the filename",
    )

    def finalize_sepa_file_creation(self, xml_root, gen_args):
        xml_string, filename = super().finalize_sepa_file_creation(xml_root, gen_args)
        if self.filename_sequence_id:
            filename = self._get_filename_with_sequence(filename)
        return xml_string, filename

    def _get_filename_with_sequence(self, previous_filename=""):
        return (
            self.filename_sequence_id.next_by_code(self.filename_sequence_id.code)
            or previous_filename
        )
