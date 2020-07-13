from app_backend.helpers.transaction_helper import populate_transactions_in_db
from app_backend.models.user_connection import SaltEdgeConnectSessionStatus

def fetch_transactions_for_accounts_linked(accounts_in_db):
    for account in accounts_in_db:
        populate_transactions_in_db(account)


def get_countries_accounts_data(app_user):
    resident_country_accounts = app_user.account_set.filter(country_id=app_user.resident_country_id)
    origin_country_accounts = app_user.account_set.filter(country_id=app_user.country_of_origin_id)
    resident_country_data = generate_country_level_data(app_user=app_user, user_accounts=resident_country_accounts,)
    origin_country_data = generate_country_level_data(app_user=app_user, user_accounts=origin_country_accounts,)
    return [
        resident_country_data,
        origin_country_data,
    ]


def generate_country_level_data(app_user, user_accounts):
    has_accounts_linked = False
    accounts_linking_in_progress = False

    if _check_for_in_progress_linking(app_user):
        accounts_linking_in_progress = True

    if len(user_accounts) > 0:
        has_accounts_linked = True
    return {
        "country_id": app_user.resident_country.id,
        "country_name": app_user.resident_country.country_name,
        "has_accounts_linked": has_accounts_linked,
        "accounts_linking_in_progress": accounts_linking_in_progress,
        "accounts_summary": {},
    }


def _check_for_in_progress_linking(app_user, country_id):
    return app_user.userconnection_set\
               .filter(country_id=country_id)\
               .filter(se_conn_session_status=SaltEdgeConnectSessionStatus.CALLBACK_SUCCESS)\
               .count() > 0

