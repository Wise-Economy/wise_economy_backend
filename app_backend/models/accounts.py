from django.db import models

from app_backend.models.banking import BankCustomerInfo


class Account(models.Model):
    id = models.IntegerField(primary_key=True)
    se_account_id = models.IntegerField()
    se_account_name = models.CharField(max_length=100)
    se_currency = models.CharField(max_length=10)
    se_balance = models.IntegerField()
    se_account_nature = models.CharField(max_length=100)
    se_account_holder_name = models.CharField(max_length=100)
    se_available_money = models.IntegerField()
    bank_customer_info_id = models.ForeignKey(BankCustomerInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    se_transaction_id = models.IntegerField()
    se_status = models.CharField(max_length=20)
    se_currency = models.CharField(max_length=10)
    se_transaction_amount = models.IntegerField()
    se_transaction_description = models.CharField(max_length=1000)
    se_transaction_category = models.CharField(max_length=20)
    se_transaction_mode = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
