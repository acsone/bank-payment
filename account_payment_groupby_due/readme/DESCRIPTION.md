This module extends the *Register Payment* wizard (`account.payment.register`)
so that payments can be grouped by invoice due date.

When paying several invoices at once, a new option *Group Payments by Due Date*
creates one payment per due date and sets each payment's date to that due date,
so each payment is dated on the day its invoices are actually due.

The option works together with the standard *Group Payments by Partner* option:
when both are enabled, payments are grouped by partner **and** due date.
