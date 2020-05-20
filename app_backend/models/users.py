import json

from django.contrib.auth.models import User
from django.db import models
from app_backend.helpers.saltedge_client import initiate_saltedge_client
from app_backend.models import BankCustomerInfo
from app_backend.models.banking import Country, BankProvider
from app_backend.helpers.saltedge_urls import *


class AppUser(User):
    se_customer_id = models.IntegerField(default=None, blank=True, null=True)
    se_identifier = models.CharField(default=None, blank=True, null=True, max_length=100)
    se_customer_type = models.CharField(default=None, blank=True, null=True, max_length=100)
    created_at = models.DateTimeField()
    last_updated = models.DateTimeField()
    country = models.ForeignKey(Country, default=None, blank=True, null=True, on_delete=models.CASCADE)
    se_customer_secret = models.CharField(default=None, blank=True, null=True, max_length=200)

    def create_saltedge_user_record(self):
        client = initiate_saltedge_client()
        payload = json.dumps({'data': {'identifier': self.email}})
        response = client.post(CREATE_SALTEDGE_USER_ACCOUNT_URL, payload)
        se_data = response.json()['data']
        self.se_customer_id = int(se_data['id'])
        self.se_identifier = se_data['identifier']
        self.se_customer_secret = se_data['secret']
        self.save()
        return True


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
    se_connection_secret = models.CharField(max_length=200)
    se_categorization = models.CharField(max_length=200)
    country_code = models.CharField(max_length=10)
