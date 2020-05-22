from django.db import models

from app_backend.models.bank_customer_info import BankCustomerInfo
from app_backend.models.user_connection import UserConnection
from app_backend.helpers.saltedge_client import initiate_saltedge_client
from app_backend.helpers.saltedge_urls import GET_TRANSACTIONS_INFO_URL
# from app_backend.helpers.transaction_helper import make_transaction_obj_from_payload


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    se_account_id = models.IntegerField()
    se_account_name = models.CharField(max_length=100)
    se_bank_account_id = models.CharField(max_length=100, default='Not Set')
    se_currency = models.CharField(max_length=10)
    se_balance = models.IntegerField()
    se_account_nature = models.CharField(max_length=100)
    se_account_holder_name = models.CharField(max_length=100)
    se_available_money = models.IntegerField()
    bank_customer_info = models.ForeignKey(BankCustomerInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user_connection = models.ForeignKey(UserConnection, on_delete=models.CASCADE, blank=True, null=True)

    def populate_transactions_in_db(self):
        client = initiate_saltedge_client()
        headers = client.generate_headers()
        headers['Customer-secret'] = self.app_user.se_customer_secret
        url = GET_TRANSACTIONS_INFO_URL + "?connection_id=" + self.user_connection.se_connection_id
        url += '&account_id=' + self.se_account_id
        response = client.get(url=url)
        transactions = response.json['data']
        transaction_models = []
        for transaction in transactions:
            transaction_models.append(make_transaction_obj_from_payload(transaction))
        self.transaction_set.bulk_create(transaction_models)


