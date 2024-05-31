# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"
    fs_storage_source_payment = fields.Selection(
        string="fs storage source payment",
        selection=[
            ("mode", "Mode"),
            ("method", "Method"),
        ],
        default="mode",
        related="company_id.fs_storage_source_payment",
        readonly=False,
    )
