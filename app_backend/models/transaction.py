from django.db import models

from app_backend.models import Account


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    se_transaction_id = models.IntegerField()
    se_status = models.CharField(max_length=20)
    se_currency = models.CharField(max_length=10)
    se_transaction_amount = models.IntegerField()
    se_transaction_description = models.CharField(max_length=1000)
    se_transaction_category = models.CharField(max_length=20)
    se_transaction_mode = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)