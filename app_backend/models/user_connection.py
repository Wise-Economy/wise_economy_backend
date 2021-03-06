import json
from datetime import datetime, timedelta
from django.db import models
from enum import Enum

from app_backend.helpers.saltedge_client import initiate_saltedge_client
from app_backend.helpers.saltedge_urls import CREATE_SALTEDGE_USER_CONNECTION_URL
from app_backend.models.bank_customer_info import BankCustomerInfo
from app_backend.models.bank_provider import BankProvider
from app_backend.models.user import AppUser
from app_backend.models.country import Country

MAX_RETRIEVAL_DAYS_SALTEDGE = 355


class SaltEdgeConnectSessionStatus(Enum):
    DEFAULT = 'UNINITIATED'
    INITIATED = 'INITIATED'
    CALLBACK_SUCCESS = 'SUCCESS'
    CALLBACK_FAILED = 'FAILED'
    ACCOUNT_FETCH_SUCCESS = 'ACCOUNTS_FETCHED'


class SaltEdgeAccountFetchStatus(Enum):
    START = 'start'
    CONNECT = 'connect'
    FETCH_ACCOUNTS = 'fetch_accounts'
    FETCH_RECENT = 'fetch_recent'
    DISCONNECT = 'disconnect'
    FINISH = 'finish'


class UserConnection(models.Model):
    id = models.AutoField(primary_key=True)
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    bank_provider = models.ForeignKey(BankProvider, on_delete=models.CASCADE, default=None, blank=True, null=True)
    bank_customer_info = models.OneToOneField(
        BankCustomerInfo,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
    )
    se_customer_id = models.CharField(max_length=200, default=None, blank=True, null=True)
    se_connection_id = models.CharField(max_length=200, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True)
    se_status = models.CharField(max_length=20, default=None, blank=True, null=True)
    se_next_refresh_at = models.DateTimeField(default=None, blank=True, null=True)
    se_last_success_at = models.DateTimeField(default=None, blank=True, null=True)
    se_connection_secret = models.CharField(max_length=200, default=None, blank=True, null=True)
    se_categorization = models.CharField(max_length=200, default=None, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    se_conn_session_status = models.CharField(
        max_length=20,
        default=SaltEdgeConnectSessionStatus.DEFAULT.value,
        blank=False,
        null=False,
    )

    def generate_saltedge_connect_session(self, country_code=None):
        payload = json.dumps(
            self._generate_payload_for_se_connect_session(
                country_code=country_code,
            )
        )
        client = initiate_saltedge_client()
        headers = client.generate_headers()
        headers['Customer-secret'] = self.app_user.se_customer_secret
        response = client.post(
            url=CREATE_SALTEDGE_USER_CONNECTION_URL,
            payload=payload,
            headers=headers,
        )
        return response.json()

    def _generate_payload_for_se_connect_session(self, country_code=None):
        # Reference : https://docs.saltedge.com/account_information/v5/#consents-object
        consent_payload = {
            'from_date': self.calculate_possible_from_date(),
            'period_days': MAX_RETRIEVAL_DAYS_SALTEDGE,
            'scopes': ['account_details', 'holder_information', 'transactions_details']
        }

        # Reference : https://docs.saltedge.com/account_information/v5/#attempts-object
        attempt_payload = {
            'automatic_fetch': True,
            'daily_refresh': True,
            'from_date': self.calculate_possible_from_date(),
            'period_days': MAX_RETRIEVAL_DAYS_SALTEDGE,
            'scopes': ['accounts', 'holder_info', 'transactions'],
            'fetched_accounts_notify': True,
            'custom_fields': {
                'user_conn_id': self.id,
            },
            'return_to': 'http://ec2-18-218-180-53.us-east-2.compute.amazonaws.com/salt_edge_connect'
        }
        return {
            'data': {
                'customer_id': str(self.app_user.se_customer_id),
                'consent': consent_payload,
                'attempt': attempt_payload,
                'allowed_countries': [country_code],
                'return_connection_id': True,
            }
        }

    @staticmethod
    def calculate_possible_from_date():
        return (datetime.now() - timedelta(days=MAX_RETRIEVAL_DAYS_SALTEDGE)) \
            .strftime("%Y-%m-%d")
