from app_backend.helpers.transaction_helper import populate_transactions_in_db


def fetch_transactions_for_accounts_linked(accounts_in_db):
    for account in accounts_in_db:
        populate_transactions_in_db(account)
