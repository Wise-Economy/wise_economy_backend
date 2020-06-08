# put public.pem & private.pem in this folder
# Add APP_ID, SECRET from saltedge into your ~/.bashrc
# Add PRIVATE_SE_PEM_FILE_PATH to your ~/.bashrc
# Install python3
# Install pip3

pip3 install virtualenv
virtualenv venv
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
source ~/.bashrc
# set up DB.
# Install postgresql.
# CREATE DATABASE wise_economy;
# GRANT ALL PRIVILEGES ON DATABASE "wise_economy" to manojt;
python manage.py migrate
./manage.py shell < ./scripts/populate_countries.py
python manage.py runserver
./manage.py shell < ./scripts/integration.py

# These steps are still is work in progress. All of them may not work.
# For the scripts populate_countries.py and integration.py, you can run them
# in the Django shell.
