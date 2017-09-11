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

from openerp import models, api, workflow


class validate_invoice_cancel(models.TransientModel):
    _name = 'validate.invoice.cancel'

    @api.multi
    def validate_cancel(self):
        context = self.env.context
        invoice_obj = self.env['account.invoice']
        invoice_id = context.get('invoice_id')
        invoice = invoice_obj.browse([invoice_id])[0]
        payment_lines = invoice_obj.get_payment_line_linked(invoice)
        payment_lines.write({'move_line_id': False})
        workflow.trg_validate(self._uid, 'account.invoice', invoice.id,
                              'invoice_cancel', self._cr)
