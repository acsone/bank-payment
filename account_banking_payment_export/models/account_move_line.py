# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2014 OpenERP S.A. (http://www.openerp.com/)
#              (C) 2014 Akretion (http://www.akretion.com/)
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

from openerp.osv import orm


class AccountMoveLine(orm.Model):
    _inherit = 'account.move.line'

    def get_balance(self, cr, uid, ids, context=None):
        """
        Return the balance of any set of move lines.

        Not to be confused with the 'balance' field on this model, which
        returns the account balance that the move line applies to.
        """
        total = 0.0
        if not ids:
            return total
        for line in self.read(
                cr, uid, ids, ['debit', 'credit'], context=context):
            total += (line['debit'] or 0.0) - (line['credit'] or 0.0)
        return total
