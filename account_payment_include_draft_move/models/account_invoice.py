# -*- coding: utf-8 -*-
#
##############################################################################
#
#     Authors: Adrien Peiffer
#    Copyright (c) 2015 Acsone SA/NV (http://www.acsone.eu)
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

from openerp import models, api, workflow, _


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def get_payment_line_linked(self, invoice):
        payment_line_obj = self.env['payment.line']
        payment_lines = []
        if invoice.move_id.id and invoice.move_id.line_id:
            inv_mv_lines = [x.id for x in invoice.move_id.line_id]
            payment_lines = payment_line_obj\
                .search([('move_line_id', 'in', inv_mv_lines)])
        return payment_lines

    @api.model
    def check_payment_line_linked(self, invoice):
        payment_lines = self.get_payment_line_linked(invoice)
        if len(payment_lines) > 0:
            return True
        else:
            return False

    @api.model
    def open_validate_invoice_cancel(self, invoice):
        wizard = self.env['validate.invoice.cancel'].create({})
        ctx = self.env.context.copy()
        ctx['invoice_id'] = invoice.id
        return {
            'name': _("Validate Invoice Cancel"),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'validate.invoice.cancel',
            'res_id': wizard.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': ctx
        }

    @api.multi
    def invoice_cancel(self):
        for invoice in self:
            if self.check_payment_line_linked(invoice):
                return self.open_validate_invoice_cancel(invoice)
            else:
                return workflow.trg_validate(self._uid, str(self._model),
                                             invoice.id, 'invoice_cancel',
                                             self._cr)
