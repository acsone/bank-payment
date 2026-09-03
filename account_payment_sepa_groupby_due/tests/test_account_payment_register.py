# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import Command
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestGroupByDueDate(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.method_line = cls.outbound_payment_method_line

    def _create_bill(self, partner, due_date, price):
        bill = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "invoice_date": "2017-01-01",
                "invoice_date_due": due_date,
                "partner_id": partner.id,
                "invoice_payment_term_id": False,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product_a.id,
                            "price_unit": price,
                            "tax_ids": [],
                        }
                    )
                ],
            }
        )
        bill.action_post()
        return bill

    def _register(self, bills, **values):
        return (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=bills.ids)
            .create(
                {
                    "payment_method_line_id": self.method_line.id,
                    **values,
                }
            )
        )

    def test_group_by_due_date_splits_by_due_date(self):
        bill_1 = self._create_bill(self.partner_a, "2017-02-01", 1000.0)
        bill_2 = self._create_bill(self.partner_a, "2017-03-01", 2000.0)

        payments = self._register(
            bill_1 + bill_2,
            group_payment=True,
            group_by_due_date=True,
        )._create_payments()

        self.assertEqual(len(payments), 2)
        self.assertEqual(
            {(p.date, p.amount) for p in payments},
            {(bill_1.invoice_date_due, 1000.0), (bill_2.invoice_date_due, 2000.0)},
        )

    def test_group_by_partner_and_due_date(self):
        bill_a1 = self._create_bill(self.partner_a, "2017-02-01", 1000.0)
        bill_a2 = self._create_bill(self.partner_a, "2017-02-01", 500.0)
        bill_a3 = self._create_bill(self.partner_a, "2017-03-01", 2000.0)
        bill_b1 = self._create_bill(self.partner_b, "2017-02-01", 300.0)

        payments = self._register(
            bill_a1 + bill_a2 + bill_a3 + bill_b1,
            group_payment=True,
            group_by_due_date=True,
        )._create_payments()

        self.assertEqual(len(payments), 3)
        self.assertEqual(
            {(p.partner_id, p.date, p.amount) for p in payments},
            {
                (self.partner_a, bill_a1.invoice_date_due, 1500.0),
                (self.partner_a, bill_a3.invoice_date_due, 2000.0),
                (self.partner_b, bill_b1.invoice_date_due, 300.0),
            },
        )

    def test_without_group_by_due_date_uses_payment_date(self):
        bill_1 = self._create_bill(self.partner_a, "2017-02-01", 1000.0)
        bill_2 = self._create_bill(self.partner_a, "2017-03-01", 2000.0)

        payments = self._register(
            bill_1 + bill_2,
            group_payment=True,
            payment_date="2017-01-15",
        )._create_payments()

        self.assertEqual(len(payments), 1)
        self.assertEqual(payments.date, date(2017, 1, 15))
