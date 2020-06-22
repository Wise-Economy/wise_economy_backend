from django.test import TestCase
from app_backend.models.user import AppUser
import mock


class AppUserTestCase(TestCase):
    dummyUserWithCustomerId = None
    dummyUserWithOutCustomerId = None
    userConnection = None
    accountDetailsForUserConnection = None

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    fake_client = MockResponse({'data': {'id': '1516', 'identifier': 'dummy', 'secret': 'dummy1234'}}, 200)

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        self.dummyUserWithCustomerId = AppUser.objects.create(email="dummy-test@gmail.com", username="test",
                                                              password="password",
                                                              se_customer_id="1234")

        self.userConnection = self.dummyUserWithCustomerId.create_user_connection_record()
        self.userConnection.se_connection_secret = "vXd8MQdFkCkN6uYGFE8aUkH5ospKjtipQohjzMrQzKo"
        self.userConnection.se_conn_session_status = "ACCOUNTS_FETCHED"
        self.userConnection.se_connection_id = 2131313131
        self.userConnection.save()

        self.userConnection.account_set.create(se_account_id=234184846951466035, se_currency="INR", se_balance=55134,
                                               se_account_nature="savings", se_account_holder_name="Sarat Chandra",
                                               se_bank_account_id=50100198874239)


        self.dummyUserWithOutCustomerId = AppUser.objects.create(email="dummy-test1@gmail.com", username="test1",
                                                                 password="password1")

    def test_return_saltedge_user_record(self):
        self.assertEqual(self.dummyUserWithCustomerId.create_or_return_saltedge_user_record(), "1234")

    @mock.patch('app_backend.models.user.create_saltedge_user', return_value=fake_client)
    def test_create_saltedge_user_record(self, create_saltedge_user):
        self.assertEqual(self.dummyUserWithOutCustomerId.create_or_return_saltedge_user_record(), "1516")

    def test_create_saltedge_user_connection_with_se_record(self):
        user_conn = self.dummyUserWithCustomerId.create_user_connection_record()
        self.assertIsNotNone(user_conn)

    def test_create_saltedge_user_connection_without_se_record(self):
        user_conn = self.dummyUserWithOutCustomerId.create_user_connection_record()
        print(user_conn)
        self.assertIsNone(user_conn)

    def test_return_balances_for_user(self):
        balance_data = self.dummyUserWithCustomerId.return_balances_for_user()
        print(balance_data)
        self.assertEqual(balance_data,'Account by the name  held by Sarat Chandra has 55134 INR')
