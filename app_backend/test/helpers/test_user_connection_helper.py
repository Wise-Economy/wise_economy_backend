from django.test import TestCase
from app_backend.models.user import AppUser
import mock
from app_backend.helpers.user_connection_helper import update_saltedge_connection_success, \
    update_if_account_fetch_success, fetch_accounts_from_saltedge

from app_backend.models.banking import Country


class UserConnectionHelperTestCase(TestCase):
    dummyUserWithCustomerId = None
    userConnection = None

    account_not_fetched = False
    account_fetched = True

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    finished_client_response = MockResponse(
        {"data":{"last_attempt":{"last_stage":{"name":"finish"}},"secret":"fake secret","provider_id":1,"provider_name":"fake bank","country_code":"IN","provider_code":"fake code"}}, 200)
    unfinished_client_response = MockResponse(
        {"data":{"last_attempt":{"last_stage":{"name":"not finished"}},"secret":"fake secret","provider_id":1,"provider_name":"fake bank","country_code":"IN","provider_code":"fake code"}}, 200)

    accounts_fetched_client_response = MockResponse({"data":{}},200)

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        self.dummyUserWithCustomerId = AppUser.objects.create(email="dummy-test@gmail.com", username="test",
                                                              password="password",
                                                              se_customer_id="1234")

        self.userConnection = self.dummyUserWithCustomerId.create_saltedge_user_connection()
        self.userConnection.se_connection_secret = "vXd8MQdFkCkN6uYGFE8aUkH5ospKjtipQohjzMrQzKo"
        self.userConnection.se_conn_session_status = "ACCOUNTS_FETCHED"
        self.userConnection.se_connection_id = 2131313131
        self.userConnection.save()
        self.userConnection.account_set.create(se_account_id=234184846951466035, se_currency="INR", se_balance=55134,
                                               se_account_nature="savings", se_account_holder_name="Sarat Chandra",
                                               se_bank_account_id=50100198874239)

        new_country = Country(country_name="India", se_country_code="IN")
        new_country.save()

    @mock.patch('app_backend.helpers.user_connection_helper.update_if_account_fetch_success',
                return_value=account_not_fetched)
    @mock.patch('app_backend.helpers.user_connection_helper.fetch_accounts_from_saltedge', return_value="")
    def test_update_saltedge_connection_success(self, update_if_account_fetch_success, fetch_accounts_from_saltedge):
        self.assertEqual(update_saltedge_connection_success(2131313131, self.userConnection.id), "Account update "
                                                                                                 "skipping as the "
                                                                                                 "accounts are not "
                                                                                                 "fetched into "
                                                                                                 "Saltedge.")

    @mock.patch('app_backend.helpers.user_connection_helper.update_if_account_fetch_success',
                return_value=account_fetched)
    @mock.patch('app_backend.helpers.user_connection_helper.fetch_accounts_from_saltedge', return_value="")
    def test_update_saltedge_connection_is_success(self, update_if_account_fetch_success, fetch_accounts_from_saltedge):
        self.assertEqual(update_saltedge_connection_success(2131313131, self.userConnection.id), "Accounts update "
                                                                                                 "successful")

    @mock.patch('app_backend.helpers.user_connection_helper.get_connections_from_saltedge',
                return_value=finished_client_response)
    def test_update_if_account_fetch_success(self, get_connections_from_saltedge):
        self.assertEqual(update_if_account_fetch_success(self.userConnection), True)

    @mock.patch('app_backend.helpers.user_connection_helper.get_connections_from_saltedge',
                return_value=unfinished_client_response)
    def test_update_if_account_fetch_failure(self, get_connections_from_saltedge):
        self.assertEqual(update_if_account_fetch_success(self.userConnection), False)

    @mock.patch('app_backend.helpers.user_connection_helper.get_accounts_from_saltedge',
                return_value=accounts_fetched_client_response)
    @mock.patch('app_backend.helpers.user_connection_helper.create_or_return_account_for_user_conn',
                return_value=accounts_fetched_client_response)
    def test_fetch_accounts_from_saltedge_success(self, get_accounts_from_saltedge, create_or_return_account_for_user_conn):
        self.assertEqual(fetch_accounts_from_saltedge(self.userConnection), None)
