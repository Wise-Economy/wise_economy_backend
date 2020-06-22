from app_backend.helpers.saltedge_client import initiate_saltedge_client
from app_backend.helpers.saltedge_urls import GET_CONNECTIONS_INFO_URL, ACCOUNT_INFO_URL
from app_backend.models.user_connection import SaltEdgeAccountFetchStatus, SaltEdgeConnectSessionStatus
from app_backend.models.bank_provider import BankProvider
from app_backend.models.user_connection import UserConnection
from app_backend.models.account import AccountDefaults
import traceback
from app_backend.helpers.account_helper import fetch_transactions_for_accounts_linked


def update_saltedge_connection_success(se_connection_id, user_connection_id):
    user_connection_obj = UserConnection.objects.get(id=user_connection_id)
    user_connection_obj.se_connection_id = se_connection_id
    user_connection_obj.se_conn_session_status = SaltEdgeConnectSessionStatus.CALLBACK_SUCCESS.value
    user_connection_obj.save()
    if update_if_account_fetch_success(user_connection_obj):
        fetch_accounts_from_saltedge(user_connection_obj)
    else:
        print("Account update skipping as the accounts are not fetched into Saltedge.")


def update_if_account_fetch_success(user_connection):
    client = initiate_saltedge_client()
    headers = client.generate_headers()
    headers['Customer-secret'] = user_connection.app_user.se_customer_secret
    response = client.get(GET_CONNECTIONS_INFO_URL + "/" + user_connection.se_connection_id)
    connection_data = response.json()['data']
    try:
        last_attempt = connection_data['last_attempt']
        fetch_status = last_attempt['last_stage']['name']
        if fetch_status == SaltEdgeAccountFetchStatus.FINISH.value:
            user_connection.bank_provider = BankProvider.create_or_return_bank_provider(
                connection_data=connection_data,
            )
            user_connection.se_connection_secret = connection_data['secret']
            user_connection.se_conn_session_status = SaltEdgeConnectSessionStatus.ACCOUNT_FETCH_SUCCESS.value
            user_connection.save()
            return True
    except Exception:
        # TODO: Handle exceptions here
        print(traceback.print_exc())
        pass

    return False


def fetch_accounts_from_saltedge(user_connection):
    # TODO: Fetch holder info -> BankCustomerInfo - Deferring this.
    client = initiate_saltedge_client()
    headers = client.generate_headers()
    headers['Customer-secret'] = user_connection.app_user.se_customer_secret
    response = client.get(ACCOUNT_INFO_URL + "?connection_id=" + user_connection.se_connection_id)
    print("response for accounts is ", response.json())
    accounts = response.json()['data']
    accounts_in_db = []
    for account in accounts:
        accounts_in_db.append(create_or_return_account_for_user_conn(user_connection, account))
    fetch_transactions_for_accounts_linked(accounts_in_db)


def create_or_return_account_for_user_conn(user_connection, saltedge_account_response):
    user_bank_account = saltedge_account_response["name"]
    user_account = user_connection.account_set.filter(se_bank_account_id=user_bank_account).first()
    if user_account is not None:
        user_connection.account_set.filter(se_bank_account_id=user_bank_account).update(
            se_balance=saltedge_account_response["balance"])
        return user_account
    se_account_holder_name = AccountDefaults.DEFAULT_ACCOUNT_HOLDER_NAME
    if "account_name" in saltedge_account_response["extra"]:
        se_account_holder_name = saltedge_account_response["extra"]["account_name"]
    elif "client_name" in saltedge_account_response["extra"]:
        se_account_holder_name = saltedge_account_response["extra"]["client_name"]
    return user_connection.account_set.create(
        se_account_id=saltedge_account_response["id"],
        se_bank_account_id=user_bank_account,
        se_balance=saltedge_account_response["balance"],
        se_currency=saltedge_account_response["currency_code"],
        se_account_nature=saltedge_account_response["nature"],
        se_account_holder_name=se_account_holder_name,
    )
