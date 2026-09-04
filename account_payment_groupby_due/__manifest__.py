# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Payment Groupby Due",
    "summary": """Group payment registration by invoice due date""",
    "category": "Banking",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/bank-payment",
    "depends": [
        "account",
    ],
    "data": [
        "wizards/account_payment_register.xml",
    ],
}
