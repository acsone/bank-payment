# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from collections import defaultdict

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import clean_context

_logger = logging.getLogger(__name__)


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    group_by_due_date = fields.Boolean(
        help="Group the payments by invoice due date and set each payment's date "
        "to that due date. Combined with 'Group Payments by Partner', payments "
        "are grouped by both partner and due date.",
    )

    def _create_payments(self):
        # The grouping is done here, at creation time only, so that the wizard's
        # batches (and therefore its whole view: editable fields, bank account,
        # memo, group-by-partner box...) keep their standard behaviour. Only the
        # payment date and the split into one payment per due date differ.
        _logger.warning(
            "GROUPBY_DUE DEBUG: group_by_due_date=%s group_payment=%s "
            "payment_date=%s lines_due=%s",
            self.group_by_due_date,
            self.group_payment,
            self.payment_date,
            [(line.id, line.move_id.invoice_date_due) for line in self.line_ids],
        )
        if not self.group_by_due_date:
            return super()._create_payments()

        self.ensure_one()

        batches = []
        for batch in self.batches:
            batch_account = self._get_batch_account(batch)
            if self.require_partner_bank_account and (
                not batch_account or not batch_account.allow_out_payment
            ):
                continue
            batches.append(batch)

        if not batches:
            raise UserError(
                _(
                    "To record payments with %(payment_method)s, the recipient bank "
                    "account must be manually validated. You should go on the partner "
                    "bank account in order to validate it.",
                    payment_method=self.payment_method_line_id.name,
                )
            )

        lines_to_pay = (
            self._get_total_amounts_to_pay(batches)["lines"]
            if self.installments_mode in ("next", "overdue", "before_date")
            else self.line_ids
        )

        due_batches = self._split_batches_by_due_date(batches, lines_to_pay)

        to_process = []
        for due_batch in due_batches:
            create_vals = self._create_payment_vals_from_batch(due_batch)
            due_date = due_batch["payment_values"]["invoice_date_due"]
            if due_date:
                create_vals["date"] = due_date
            _logger.warning(
                "GROUPBY_DUE DEBUG: sub-batch due_date=%s -> create_vals date=%s",
                due_date,
                create_vals["date"],
            )
            to_process.append(
                {
                    "create_vals": create_vals,
                    "to_reconcile": due_batch["lines"],
                    "batch": due_batch,
                }
            )

        lines = sum(
            (due_batch["lines"] for due_batch in due_batches),
            self.env["account.move.line"],
        )
        from_sibling_companies = self._from_sibling_companies(lines)
        if (
            from_sibling_companies
            and lines.company_id.root_id not in self.env.companies
        ):
            self.env.context = {**self.env.context, "dont_redirect_to_payments": True}

        wizard = self.sudo() if from_sibling_companies else self
        payments = wizard.with_context(clean_context(self.env.context))._init_payments(  # pylint: disable=context-overridden
            to_process, edit_mode=False
        )
        wizard._post_payments(to_process, edit_mode=False)
        wizard._reconcile_payments(to_process, edit_mode=False)
        return payments.sudo(flag=False)

    def _split_batches_by_due_date(self, batches, lines_to_pay):
        """Split each standard batch into one sub-batch per invoice due date.

        When 'group_payment' is set, lines sharing a due date are merged into a
        single payment (grouping by partner AND due date); otherwise each journal
        item stays on its own payment, dated on its due date.
        """
        due_batches = []
        for batch_result in batches:
            groups = defaultdict(lambda: self.env["account.move.line"])
            for line in batch_result["lines"] & lines_to_pay:
                group_key = (
                    line.move_id.invoice_date_due
                    if self.group_payment
                    else (line.id, line.move_id.invoice_date_due)
                )
                groups[group_key] += line
            for group_lines in groups.values():
                balance = sum(group_lines.mapped("balance"))
                due_batches.append(
                    {
                        **batch_result,
                        "payment_values": {
                            **batch_result["payment_values"],
                            "payment_type": "inbound" if balance > 0 else "outbound",
                            "invoice_date_due": group_lines[0].move_id.invoice_date_due,
                        },
                        "lines": group_lines,
                    }
                )
        return due_batches
