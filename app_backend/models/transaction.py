from django.db import models
from django.contrib.postgres.fields import JSONField
from app_backend.models.account import Account


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    se_transaction_id = models.IntegerField()
    se_status = models.CharField(max_length=20)
    se_currency = models.CharField(max_length=10)
    se_transaction_amount = models.IntegerField()
    se_transaction_description = models.CharField(max_length=1000)
    se_transaction_category = models.CharField(max_length=20)
    se_transaction_mode = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    balance_snapshot = models.IntegerField()
    se_mode = models.CharField(max_length=20)
    se_status = models.CharField(max_length=20)
    se_made_on = models.DateTimeField
    payee_info = JSONField()
