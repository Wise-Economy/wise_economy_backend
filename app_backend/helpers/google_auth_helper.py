import requests
import traceback

VERIFY_URL = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token='


def verify_google_token(token, email, google_id):
    try:
        full_url = VERIFY_URL + token
        request = requests.get(full_url)
        response = request.json()
        if response['email'] == email and response['user_id'] == google_id:
            return True
    except Exception:
        print(traceback.format_exc())
    return True
