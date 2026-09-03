BUSINESS NEED:

Companies paying vendor bills through SEPA credit transfers often want each
transfer to be executed by the bank on the invoice due date, rather than all on
the same payment date. When registering a payment for many invoices at once,
the standard wizard uses a single payment date for the whole batch.

APPROACH:

This module adds a *Group Payments by Due Date* option to the standard
*Register Payment* wizard. Lines are additionally grouped by their invoice due
date, and each resulting payment is dated on that due date. It reuses Odoo's
existing batching mechanism, so it composes naturally with the standard
*Group Payments by Partner* option.
