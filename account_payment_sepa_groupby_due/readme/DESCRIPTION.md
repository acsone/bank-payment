This module extends the *Register Payment* wizard (`account.payment.register`)
so that SEPA payments can be grouped by invoice due date.

When paying several invoices with a SEPA payment method, a new option
*Group Payments by Due Date* creates one payment per due date and sets each
payment's date to that due date, so the transfers are executed by the bank on
the day each invoice is actually due.

The option works together with the standard *Group Payments by Partner* option:
when both are enabled, payments are grouped by partner **and** due date.
