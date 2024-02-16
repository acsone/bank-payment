# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountPaymentMethod(models.Model):

    _inherit = "account.payment.method"

    storage_id = fields.Many2one(
        comodel_name="fs.storage",
        string="Storage",
        help="Storage where to put the file after generation",
    )
