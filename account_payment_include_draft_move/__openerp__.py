# -*- coding: utf-8 -*-
#
##############################################################################
#
#     Authors: Adrien Peiffer
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

{
    "name": "Account Payment Draft Move",
    "version": "8.0.1.0.0",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "http://www.acsone.eu",
    "images": [],
    "category": "Accounting",
    "depends": ["account_banking_payment_export",
                "account_default_draft_move",
                ],
    "data": [
        'views/account_invoice_view.xml',
        'wizard/validate_invoice_cancel_view.xml',
        ],
    "demo": [],
    "test": [],
    "licence": "AGPL-3",
    "installable": True,
    "active": False,
}
