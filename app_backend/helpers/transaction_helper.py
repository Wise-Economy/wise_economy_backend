from app_backend.helpers.saltedge_client import initiate_saltedge_client
from app_backend.helpers.saltedge_urls import GET_TRANSACTIONS_INFO_URL
from app_backend.models.transaction import Transaction


def make_transaction_obj_from_payload(transaction_payload, account_id):
    return Transaction(
        se_transaction_id=transaction_payload['id'],
        se_mode=transaction_payload['mode'],
        se_status=transaction_payload['status'],
        se_made_on=transaction_payload['made_on'],
        se_currency=transaction_payload['currency_code'],
        se_transaction_amount=transaction_payload['amount'],
        se_transaction_description=transaction_payload['description'],
        se_transaction_category=transaction_payload['category'],
        balance_snapshot=transaction_payload['extra']['account_balance_snapshot'],
        payee_info=transaction_payload['extra'],
        account_id=account_id,
    )


def populate_transactions_in_db(account):
    client = initiate_saltedge_client()
    headers = client.generate_headers()
    headers['Customer-secret'] = account.user_connection.app_user.se_customer_secret
    url = GET_TRANSACTIONS_INFO_URL + "?connection_id=" + account.user_connection.se_connection_id
    url += '&account_id=' + account.se_account_id
    response = client.get(url=url)
    transactions = response.json()['data']
    transaction_models = []
    for transaction in transactions:
        transaction_models.append(make_transaction_obj_from_payload(transaction, account.id))
    Transaction.objects.bulk_create(transaction_models, ignore_conflicts=True)
