from django.db import models


class Country(models.Model):
    id = models.IntegerField(primary_key=True)
    currency = models.CharField(max_length=10)
    country_name = models.CharField(max_length=20)
    se_country_id = models.IntegerField()
    se_country_code = models.CharField(max_length=10)
    country_flag_icon_url = models.CharField(max_length=1024)


class BankProvider(models.Model):
    id = models.IntegerField(primary_key=True)
    bank_name = models.CharField(max_length=100)
    bank_country = models.CharField(max_length=10)
    provider_name = models.CharField(max_length=150)
    se_provider_code = models.CharField(max_length=150)
    se_country_code = models.CharField(max_length=10)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class BankCustomerInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    origin_country = models.CharField(max_length=20)
    account_type = models.CharField(max_length=20)
    residence_country = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    bank_provider = models.ForeignKey(BankProvider, on_delete=models.CASCADE)