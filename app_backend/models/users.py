from django.contrib.auth.models import User
from django.db import models

from app_backend.models import BankCustomerInfo
from app_backend.models.banking import Country, BankProvider


class AppUser(User):
    se_customer_id = models.IntegerField()
    se_identifier = models.CharField(max_length=100)
    se_customer_type = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    last_updated = models.DateTimeField()
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)


class UserConnection(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_provider_id = models.ForeignKey(BankProvider, on_delete=models.CASCADE)
    bank_customer_info = models.OneToOneField(BankCustomerInfo, on_delete=models.CASCADE)
    se_customer_id = models.IntegerField()
    se_identifier = models.CharField(max_length=100)
    provider_name = models.CharField(max_length=150)
    se_provider_code = models.CharField(max_length=150)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()
    se_status = models.CharField(max_length=20)
    se_next_refresh_at = models.DateTimeField()
    se_last_success_at = models.DateTimeField()
    se_provider_id = models.IntegerField()
    se_secret = models.CharField(max_length=200)
    se_categorization = models.CharField(max_length=200)
    country_code = models.CharField(max_length=10)