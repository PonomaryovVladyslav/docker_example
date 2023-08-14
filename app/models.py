"""File to describe models for ORM."""
from django.db import models

TRANSACTION_TYPE = (
    ('i', 'Income'),
    ('e', 'Expense')
)


class Transaction(models.Model):
    """Class mapping for each transaction object."""
    date = models.DateField()
    type = models.CharField(max_length=1, choices=TRANSACTION_TYPE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    expense_category = models.CharField(max_length=100, blank=True, null=True)
    job_address = models.CharField(max_length=100, blank=True, null=True)
