# from app_backend.models import transaction
#
#
# def make_transaction_obj_from_payload(transaction_payload):
#     return transaction.Transaction(
#         se_transaction_id=transaction_payload['id'],
#         se_mode=transaction_payload['mode'],
#         se_status=transaction_payload['status'],
#         se_made_on=transaction_payload['made_on'],
#         se_currency=transaction_payload['currency'],
#         se_transaction_amount=transaction_payload['amount'],
#         se_transaction_description=transaction_payload['description'],
#         se_transaction_category=transaction_payload['category'],
#         balance_snapshot=transaction_payload['account_balance_snapshot'],
#         payee_info=transaction_payload['extra'],
#     )
