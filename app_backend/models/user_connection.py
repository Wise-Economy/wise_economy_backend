import json
from datetime import datetime, timedelta
import traceback
from django.db import models
from enum import Enum

from app_backend.helpers.saltedge_client import initiate_saltedge_client
from app_backend.helpers.saltedge_urls import CREATE_SALTEDGE_USER_CONNECTION_URL
from app_backend.helpers.saltedge_urls import ACCOUNT_INFO_URL, GET_CONNECTIONS_INFO_URL
from app_backend.models.bank_customer_info import BankCustomerInfo
from app_backend.models.bank_provider import BankProvider
from app_backend.models.user import AppUser

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
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(default=None, blank=True, null=True)
    se_status = models.CharField(max_length=20, default=None, blank=True, null=True)
    se_next_refresh_at = models.DateTimeField(default=None, blank=True, null=True)
    se_last_success_at = models.DateTimeField(default=None, blank=True, null=True)
    se_connection_secret = models.CharField(max_length=200, default=None, blank=True, null=True)
    se_categorization = models.CharField(max_length=200, default=None, blank=True, null=True)
    country_code = models.CharField(max_length=10, default=None, blank=True, null=True)
    se_conn_session_status = models.CharField(
        max_length=20,
        default=SaltEdgeConnectSessionStatus.DEFAULT.value,
        blank=False,
        null=False,
    )

    def generate_saltedge_connect_session(self):
        payload = json.dumps(self._generate_payload_for_se_connect_session())
        client = initiate_saltedge_client()
        headers = client.generate_headers()
        headers['Customer-secret'] = self.app_user.se_customer_secret
        response = client.post(
            url=CREATE_SALTEDGE_USER_CONNECTION_URL,
            payload=payload,
            headers=headers,
        )
        return response

    def _generate_payload_for_se_connect_session(self):
        # Reference : https://docs.saltedge.com/account_information/v5/#consents-object
        consent_payload = {
            'from_date': self.calculate_possible_from_date(),
            'period_days': MAX_RETRIEVAL_DAYS_SALTEDGE,
            'scopes': ['account_details', 'transactions_details']
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
                'return_connection_id': True,
            }
        }

    def update_if_account_fetch_success(self):
        client = initiate_saltedge_client()
        headers = client.generate_headers()
        headers['Customer-secret'] = self.app_user.se_customer_secret
        response = client.get(GET_CONNECTIONS_INFO_URL + "/" + self.se_connection_id)
        connection_data = response.json()['data']
        try:
            last_attempt = connection_data['last_attempt']
            fetch_status = last_attempt['last_stage']['name']
            if fetch_status == SaltEdgeAccountFetchStatus.FINISH:
                self.bank_provider = BankProvider.create_or_return_bank_provider(
                    connection_data=connection_data,
                )
                self.se_connection_secret = connection_data['secret']
                self.se_conn_session_status = SaltEdgeConnectSessionStatus.ACCOUNT_FETCH_SUCCESS.value
                self.save()
                return True
        except Exception:
            # TODO: Handle exceptions here
            print(traceback.print_exc())
            pass

        return False

    def fetch_accounts_from_saltedge(self):
        # TODO: Fetch holder info -> BankCustomerInfo - Deferring this.
        client = initiate_saltedge_client()
        headers = client.generate_headers()
        headers['Customer-secret'] = self.app_user.se_customer_secret
        response = client.get(ACCOUNT_INFO_URL + "?connection_id=" + self.se_conn)
        accounts = response.json()['data']
        for account in accounts:
            self.create_account_for_user_conn(account)
            # TODO: Fetch transactions -> Transaction

    def create_account_for_user_conn(self, account):
        self.account_set.create(
            se_account_id=account["id"],
            se_bank_account_id=account["name"],
            se_balance=account["balance"],
            se_currency=account["currency"],
            se_account_nature=account["nature"],
            se_available_money=account["extra"]["available_amount"],
            se_account_holder_name=account["extra"]["account_name"],
        )

    @staticmethod
    def update_saltedge_connection_success(se_connection_id, user_connection_id):
        user_connection_obj = UserConnection.objects.get(id=user_connection_id)
        user_connection_obj.se_connection_id = se_connection_id
        user_connection_obj.se_conn_session_status = SaltEdgeConnectSessionStatus.CALLBACK_SUCCESS.value
        user_connection_obj.save()
        if user_connection_obj.update_if_account_fetch_success():
            user_connection_obj.fetch_accounts_from_saltedge()
        else:
            print("Account update skipping as the accounts are not fetched into Saltedge.")

    @staticmethod
    def calculate_possible_from_date():
        return (datetime.now() - timedelta(days=MAX_RETRIEVAL_DAYS_SALTEDGE)) \
            .strftime("%Y-%m-%d")
