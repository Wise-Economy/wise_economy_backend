from app_backend.helpers.transaction_helper import populate_transactions_in_db


def fetch_transactions_for_accounts_linked(accounts_in_db):
    for account in accounts_in_db:
        populate_transactions_in_db(account)


def get_countries_accounts_data(app_user):
    app_user.account_set
    return [
        {
            "country_id": app_user.resident_country.id,
            "country_name": app_user.resident_country.country_name,
            "has_accounts_linked": False,
        },
        {
            "country_id": app_user.country_of_origin.id,
            "country_name": app_user.country_of_origin.country_name,
            "has_accounts_linked": False,
        },
    ]
