# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    group_by_due_date = fields.Boolean(
        help="Group the SEPA payments by invoice due date and set each payment's "
        "date to that due date. Combined with 'Group Payments by Partner', "
        "payments are grouped by both partner and due date.",
    )

    @api.depends("group_by_due_date")
    def _compute_batches(self):
        # 'group_by_due_date' widens the batch key (see '_get_line_batch_key'),
        # so batches must be recomputed when the flag is toggled.
        return super()._compute_batches()

    def _get_line_batch_key(self, line):
        key = super()._get_line_batch_key(line)
        if self.group_by_due_date:
            key["invoice_date_due"] = line.move_id.invoice_date_due
        return key

    def _create_payment_vals_from_wizard(self, batch_result):
        payment_vals = super()._create_payment_vals_from_wizard(batch_result)
        self._set_due_date_on_payment_vals(payment_vals, batch_result)
        return payment_vals

    def _create_payment_vals_from_batch(self, batch_result):
        payment_vals = super()._create_payment_vals_from_batch(batch_result)
        self._set_due_date_on_payment_vals(payment_vals, batch_result)
        return payment_vals

    def _set_due_date_on_payment_vals(self, payment_vals, batch_result):
        due_date = batch_result["payment_values"].get("invoice_date_due")
        if self.group_by_due_date and due_date:
            payment_vals["date"] = due_date
