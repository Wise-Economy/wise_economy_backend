import json

from django.contrib.auth.models import User
from django.db import models
from app_backend.models.country import Country
from app_backend.helpers.saltedge_client import initiate_saltedge_client
from app_backend.helpers.saltedge_urls import *
from datetime import datetime
import traceback


class USER_DEFAULTS:
    DEFAULT_PASSWORD = "WhateverPassword12#"


class SIGN_IN_METHODS:
    GOOGLE_SIGN_IN = "google"
    EMAIL_SIGN_IN = "email"
    APPLE_ID_SIGN_IN = "apple"


def create_saltedge_user(payload):
    client = initiate_saltedge_client()
    response = client.post(CREATE_SALTEDGE_CUSTOMER_ACCOUNT_URL, payload)
    return response


class AppUser(User):
    se_customer_id = models.CharField(max_length=200, blank=True, null=True)
    se_identifier = models.CharField(default=None, blank=True, null=True, unique=True, max_length=100)
    se_customer_type = models.CharField(default=None, blank=True, null=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    resident_country = models.ForeignKey(
        Country,
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='resident_country'
    )
    se_customer_secret = models.CharField(default=None, blank=True, null=True, max_length=200)
    google_id = models.CharField(default=None, blank=True, null=True, max_length=200)
    profile_photo = models.CharField(default=None, blank=True, null=True, max_length=200)
    full_name = models.CharField(default=None, blank=True, null=True, max_length=200)
    sign_in_method = models.CharField(default=None, blank=True, null=True, max_length=20)
    phone_number = models.CharField(default=None, blank=True, null=True, max_length=20)
    country_of_origin = models.ForeignKey(
        Country,
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='country_of_origin',
    )

    def create_or_return_saltedge_user_record(self):
        if self.se_customer_id is not None:
            return self.se_customer_id
        else:
            payload = json.dumps({'data': {'identifier': self.email}})
            response = create_saltedge_user(payload)
            print("response is ", response.json())
            se_data = response.json()['data']
            self.se_customer_id = se_data['id']
            self.se_identifier = se_data['identifier']
            self.se_customer_secret = se_data['secret']
            self.save()
            return self.se_customer_id

    def create_user_connection_record(self):
        if self.se_customer_id is not None:
            user_conn = self.userconnection_set.create(
                se_customer_id=self.se_customer_id,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            user_conn.save()
            return user_conn

    def return_balances_for_user(self):
        for user_conn in self.userconnection_set.all():
            accounts = user_conn.account_set.all()
            for account in accounts:
                return account.print_details()

    def get_user_details(self):
        user_details = {
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth,
            "phone_number": self.phone_number,
            "email": self.email,
            "profile_photo": self.profile_photo,
        }
        if self.resident_country:
            user_details["residence_country"] = {
                "country_id": self.resident_country.id,
                "country_name": self.resident_country.country_name,
            }
        return user_details

    def register_user_details(self, user_details):
        try:
            self.full_name = user_details['full_name']
            self.date_of_birth = user_details['date_of_birth']
            self.phone_number = user_details['phone_number']
            self.email = user_details['email']
            self.resident_country = Country.objects.get(
                id=user_details['residence_country']['country_id']
            )
            india = Country.objects.get(se_country_code='IN')
            # NOTE: Enabling this for only Indian expats.
            # Might feel cute later, open it up for expats of different origins.
            self.country_of_origin = india
            self.profile_photo = user_details['profile_photo']
            self.save()
            return True
        except Exception:
            print(traceback.format_exc())
            return False

    @staticmethod
    def get_by_user(user):
        # This method returns the corresponding AppUser record using django auth user record.
        return AppUser.objects.get(id=user.id)

