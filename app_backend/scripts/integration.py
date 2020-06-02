from app_backend.models.user import AppUser
import random
from app_backend.helpers.user_connection_helper import update_saltedge_connection_success

random_int1 = random.randint(1, 10000)
random_int2 = random.randint(1, 10000)
app_user = AppUser.objects.create(
    email=f"random.{random_int1}{random_int2}@whatever.com",
    username=f"{random_int1}.{random_int2}",
    password=f"{random_int1}.{random_int2}",
)
print("Created a app user in the db with id: " + str(app_user.id) + "\n")
print("Created a saltedge record for the user id : " + str(
    app_user.id) + ": " + app_user.create_or_return_saltedge_user_record())
user_connection = app_user.create_saltedge_user_connection()
print("Created user connection object, id : " + str(user_connection.id))
connect_session_response = user_connection.generate_saltedge_connect_session()
print("Created saltedge connect session..")
print(connect_session_response.json())

se_conn_id = input("Please enter the saltedge connection id : ")
update_saltedge_connection_success(se_connection_id=se_conn_id, user_connection_id=user_connection.id)
app_user.return_balances_for_user()
