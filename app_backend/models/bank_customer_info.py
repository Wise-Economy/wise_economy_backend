from django.db import models

from app_backend.models.bank_provider import BankProvider


class BankCustomerInfo(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    origin_country = models.CharField(max_length=20)
    account_type = models.CharField(max_length=20)
    residence_country = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    bank_provider = models.ForeignKey(BankProvider, on_delete=models.CASCADE)