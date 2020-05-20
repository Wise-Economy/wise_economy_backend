import json

from django.contrib.auth.models import User
from django.db import models
from app_backend.helpers.saltedge_client import initiate_saltedge_client
from app_backend.models.banking import Country
from app_backend.helpers.saltedge_urls import *
from datetime import datetime


class AppUser(User):
    se_customer_id = models.BigIntegerField(default=None, blank=True, null=True)
    se_identifier = models.CharField(default=None, blank=True, null=True, max_length=100)
    se_customer_type = models.CharField(default=None, blank=True, null=True, max_length=100)
    created_at = models.DateTimeField()
    last_updated = models.DateTimeField()
    country = models.ForeignKey(Country, default=None, blank=True, null=True, on_delete=models.CASCADE)
    se_customer_secret = models.CharField(default=None, blank=True, null=True, max_length=200)

    def create_saltedge_user_record(self):
        client = initiate_saltedge_client()
        payload = json.dumps({'data': {'identifier': self.email}})
        # TODO : Verify if  this exists and then post
        response = client.post(CREATE_SALTEDGE_CUSTOMER_ACCOUNT_URL, payload)
        se_data = response.json()['data']
        self.se_customer_id = int(se_data['id'])
        self.se_identifier = se_data['identifier']
        self.se_customer_secret = se_data['secret']
        self.save()
        return True

    def create_saltedge_user_connection(self):
        user_conn = self.userconnection_set.create(
            se_customer_id=self.se_customer_id,
            se_identifier=self.se_identifier,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        user_conn.save()


