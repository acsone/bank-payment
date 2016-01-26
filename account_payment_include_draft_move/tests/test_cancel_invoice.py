# -*- coding: utf-8 -*-
#
##############################################################################
#
#    Authors: Adrien Peiffer
#    Copyright (c) 2014 Acsone SA/NV (http://www.acsone.eu)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import openerp.tests.common as common
from openerp import workflow, fields


def create_simple_invoice(self, date):
    journal_id = self.ref('account.sales_journal')
    partner_id = self.ref('base.res_partner_4')
    product_id = self.ref('product.product_product_4')
    return self.env['account.invoice']\
        .create({'partner_id': partner_id,
                 'account_id':
                 self.ref('account.a_pay'),
                 'journal_id':
                 journal_id,
                 'date_invoice': date,
                 'date_due': date,
                 'type': 'in_invoice',
                 'invoice_line': [(0, 0, {'name': 'test',
                                          'account_id':
                                          self.ref('account.a_expense'),
                                          'price_unit': 2000.00,
                                          'quantity': 1,
                                          'product_id': product_id,
                                          }
                                   )
                                  ],
                 })


class TestCancelInvoice(common.TransactionCase):

    def setUp(self):
        super(TestCancelInvoice, self).setUp()
        self.context = self.registry("res.users").context_get(self.cr,
                                                              self.uid)

    def test_cancel_invoice(self):
        date = fields.Date.today()
        invoice = create_simple_invoice(self, date)
        workflow.trg_validate(self.uid, 'account.invoice', invoice.id,
                              'invoice_open', self.cr)
        # I check if created invoice isn't linked with a payment line
        invoice_obj = self.env['account.invoice']
        payment_lines = invoice_obj.get_payment_line_linked(invoice)
        self.assertTrue(len(payment_lines) == 0,
                        "Invoice is linked with a payment line")
        # I click on cancel invoice button
        res = invoice.invoice_cancel()
        # I check if the wizard is correctly instantiated
        self.assertFalse(isinstance(res, dict), "wizard action is returned")
        # I check if invoice is cancelled
        self.assertEqual(invoice.state, 'cancel', 'Invoice isn\'t cancelled')

    def test_payment_cancel_invoice(self):
        date = fields.Date.today()
        invoice = create_simple_invoice(self, date)
        workflow.trg_validate(self.uid, 'account.invoice', invoice.id,
                              'invoice_open', self.cr)
        payment_order_create_obj = self.env['payment.order.create']
        account_payment_id = self.ref('account_payment.payment_order_1')
        payment_order_create = payment_order_create_obj.create(
            {'duedate': date,
             'populate_results': True})
        ctx = self.context.copy()
        ctx.update({'active_id': account_payment_id})
        res = payment_order_create.with_context(ctx).search_entries()
        payment_order_create.entries = res['context']['line_ids']
        payment_order_create.with_context(ctx).create_payment()
        # I check if created invoice is linked with a payment line
        invoice_obj = self.env['account.invoice']
        payment_lines = invoice_obj.get_payment_line_linked(invoice)
        self.assertTrue(len(payment_lines) > 0,
                        "Invoice isn't on a payment line")
        # I click on cancel invoice button
        res = invoice.invoice_cancel()
        # I check if the wizard is correctly instantiated
        self.assertTrue(isinstance(res, dict), "Not return wizard action")
        ctx = res.get('context')
        wizard_id = res.get('res_id')
        wizard_obj = self.env['validate.invoice.cancel']
        wizard = wizard_obj.browse([wizard_id])[0]
        # click on force cancel button
        wizard.with_context(ctx).validate_cancel()
        # I check if invoice is cancelled
        self.assertEqual(invoice.state, 'cancel', 'Invoice isn\'t cancelled')
