from django.db import models

from app_backend.models.bank_customer_info import BankCustomerInfo
from app_backend.models.user_connection import UserConnection


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    se_account_id = models.CharField(max_length=100)
    se_account_name = models.CharField(max_length=100)
    se_bank_account_id = models.CharField(max_length=100, unique=True, default='Not Set')
    se_currency = models.CharField(max_length=10)
    se_balance = models.IntegerField()
    se_account_nature = models.CharField(max_length=100)
    se_account_holder_name = models.CharField(max_length=100)
    se_available_money = models.IntegerField(blank=True, null=True)
    # TODO : Once holding info access is available, populate this feature.
    bank_customer_info = models.ForeignKey(BankCustomerInfo, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_connection = models.ForeignKey(UserConnection, on_delete=models.CASCADE, blank=True, null=True)

    def print_details(self):
        return(f"Account by the name {self.se_account_name} held by "
              f"{self.se_account_holder_name} has {self.se_balance} {self.se_currency}")

