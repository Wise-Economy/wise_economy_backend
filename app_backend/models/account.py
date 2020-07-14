from django.db import models

from app_backend.models.bank_customer_info import BankCustomerInfo
from app_backend.models.user_connection import UserConnection
from app_backend.models.user import AppUser
from app_backend.models.country import Country


class AccountDefaults:
    DEFAULT_ACCOUNT_HOLDER_NAME = "NAME-UNDETECTED"


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    se_account_id = models.CharField(max_length=100)
    se_account_name = models.CharField(max_length=100)
    se_bank_account_id = models.CharField(max_length=100, default='Not Set')
    se_currency = models.CharField(max_length=10)
    se_balance = models.FloatField()
    se_account_nature = models.CharField(max_length=100)
    se_account_holder_name = models.CharField(max_length=100)
    se_available_money = models.FloatField(blank=True, null=True)
    # TODO : Once holding info access is available, populate this feature.
    bank_customer_info = models.ForeignKey(BankCustomerInfo, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE, blank=True, null=True)
    user_connection = models.ForeignKey(UserConnection, on_delete=models.CASCADE, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    # TODO : Credit Card : Clarify meanings below.
    card_type = models.CharField(max_length=20, blank=True, null=True,)
    available_credit = models.FloatField(default=0.0)
    closing_balance = models.FloatField(default=0.0)
    card_expiry_date = models.DateField(null=True, blank=True,)
    # TODO : Deposits : Clarify meaning of the below fields and add detailed comments.
    interest_rate = models.FloatField(default=0.0)
    deposit_open_date = models.DateField(null=True, blank=True,)
    deposit_expiry_date = models.DateField(null=True, blank=True,)
    deposit_type = models.CharField(max_length=20, blank=True, null=True,)



    class Meta:
        unique_together = ("app_user", "se_bank_account_id")

    def print_details(self):
        return (f"Account by the name {self.se_account_name} held by "
                f"{self.se_account_holder_name} has {self.se_balance} {self.se_currency}")
