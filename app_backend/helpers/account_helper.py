from app_backend.helpers.transaction_helper import populate_transactions_in_db


def fetch_transactions_for_accounts_linked(accounts_in_db):
    for account in accounts_in_db:
        populate_transactions_in_db(account)


def get_countries_accounts_data(app_user):
    resident_country_accounts = app_user.account_set.filter(country_id=app_user.resident_country_id)
    origin_country_accounts = app_user.account_set.filter(country_id=app_user.country_of_origin_id)
    resident_country_data = generate_resident_country_data(app_user=app_user, user_accounts=resident_country_accounts,)
    origin_country_data = generate_origin_country_data(app_user=app_user, user_accounts=origin_country_accounts,)
    return [
        resident_country_data,
        origin_country_data,
    ]


def generate_resident_country_data(app_user, user_accounts):
    has_accounts_linked = False
    if len(user_accounts) > 0:
        has_accounts_linked = True
    return {
        "country_id": app_user.resident_country.id,
        "country_name": app_user.resident_country.country_name,
        "has_accounts_linked": has_accounts_linked,
        "accounts_summary": {},
    }


def generate_origin_country_data(app_user, user_accounts):
    has_accounts_linked = False
    if len(user_accounts) > 0:
        has_accounts_linked = True
    return {
        "country_id": app_user.country_of_origin.id,
        "country_name": app_user.country_of_origin.country_name,
        "has_accounts_linked": has_accounts_linked,
        "accounts_summary": {},
    }
