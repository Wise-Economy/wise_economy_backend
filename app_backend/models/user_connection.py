import json
from datetime import datetime, timedelta

from django.db import models

from app_backend.helpers.saltedge_client import initiate_saltedge_client
from app_backend.helpers.saltedge_urls import CREATE_SALTEDGE_USER_CONNECTION_URL
from app_backend.models import AppUser, BankProvider, BankCustomerInfo

MAX_RETRIEVAL_DAYS_SALTEDGE = 355


class UserConnection(models.Model):
    id = models.AutoField(primary_key=True)
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    bank_provider = models.ForeignKey(BankProvider, on_delete=models.CASCADE, default=None, blank=True, null=True)
    bank_customer_info = models.OneToOneField(BankCustomerInfo, on_delete=models.CASCADE, default=None, blank=True, null=True)
    se_customer_id = models.BigIntegerField()
    se_identifier = models.CharField(max_length=100)
    provider_name = models.CharField(max_length=150, default=None, blank=True, null=True)
    se_provider_code = models.CharField(max_length=150, default=None, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(default=None, blank=True, null=True)
    se_status = models.CharField(max_length=20, default=None, blank=True, null=True)
    se_next_refresh_at = models.DateTimeField(default=None, blank=True, null=True)
    se_last_success_at = models.DateTimeField(default=None, blank=True, null=True)
    se_provider_id = models.IntegerField(default=None, blank=True, null=True)
    se_connection_secret = models.CharField(max_length=200, default=None, blank=True, null=True)
    se_categorization = models.CharField(max_length=200, default=None, blank=True, null=True)
    country_code = models.CharField(max_length=10, default=None, blank=True, null=True)

    def generate_saltedge_connect_session(self):
        payload = json.dumps(self._generate_payload())
        client = initiate_saltedge_client()
        headers = client.generate_headers()
        headers['Customer-secret'] = self.app_user.se_customer_secret
        response = client.post(
            url=CREATE_SALTEDGE_USER_CONNECTION_URL,
            payload=payload,
            headers=headers,
        )
        return response

    def _generate_payload(self):
        # Reference : https://docs.saltedge.com/account_information/v5/#consents-object
        consent_payload = {
            'from_date': self.calculate_possible_from_date(),
            'period_days': MAX_RETRIEVAL_DAYS_SALTEDGE,
            'scopes': ['account_details', 'transactions_details']
        }

        # Reference : https://docs.saltedge.com/account_information/v5/#attempts-object
        attempt_payload = {
            'from_date': self.calculate_possible_from_date(),
            'period_days': MAX_RETRIEVAL_DAYS_SALTEDGE,
            'scopes': ['accounts', 'holder_info', 'transactions'],
        }
        return {
            'data': {
                'customer_id': str(self.app_user.se_customer_id),
                'consent': consent_payload,
                'attempt': attempt_payload
            }
        }

    @staticmethod
    def calculate_possible_from_date():
        return (datetime.now() - timedelta(days=MAX_RETRIEVAL_DAYS_SALTEDGE))\
            .strftime("%Y-%m-%d")