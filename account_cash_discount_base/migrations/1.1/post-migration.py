# -*- encoding: utf-8 -*-
import logging
from openerp import SUPERUSER_ID
from openerp.modules.registry import RegistryManager

uid = SUPERUSER_ID

__name__ = 'Compute discount field on account invoice'
_logger = logging.getLogger(__name__)


def compute_discount(cr, registry):
    invoice_obj =  registry['account.invoice']
    inv_ids = invoice_obj.search(cr, uid, [('type', 'in', ('in_invoice', 'out_invoice'))])
    for inv in invoice_obj.browse(cr, uid, inv_ids):
        if inv.discount_amount != 0.0:
            discount = inv.amount_total - inv.discount_amount
        else:
            discount = 0.0
        invoice_obj.write(cr, uid, [inv.id], {'discount': discount})


def remove_unnecessary_date(cr, registry): 
    invoice_obj =  registry['account.invoice']
    inv_ids = invoice_obj.search(cr, uid, [('discount_due_date', '!=', False),
                                           ('discount', '=', 0)])
    invoice_obj.write(cr, uid, inv_ids, {'discount_due_date': False})

def migrate(cr, version):
    if not version:
        # it is the installation of the module
        return
    registry = RegistryManager.get(cr.dbname)
    compute_discount(cr, registry)
    remove_unnecessary_date(cr, registry)
