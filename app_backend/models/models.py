from django.db import models


class Country(models.Model):
    id = models.IntegerField(primary_key=True)
    currency = models.CharField(max_length=10)
    country_name = models.CharField(max_length=20)
    se_country_id = models.IntegerField()
    se_country_code = models.CharField(max_length=10)
    country_flag_icon_url = models.CharField(max_length=1024)


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    se_customer_id = models.IntegerField()
    se_identifier = models.CharField(max_length=100)
    se_customer_type = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    last_updated = models.DateTimeField()
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)


class BankProvider(models.Model):
    id = models.IntegerField(primary_key=True)
    bank_name = models.CharField(max_length=100)
    bank_country = models.CharField(max_length=10)
    provider_name = models.CharField(max_length=150)
    se_provider_code = models.CharField(max_length=150)
    se_country_code = models.CharField(max_length=10)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)


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
    bank_provider_id = models.ForeignKey(BankProvider, on_delete=models.CASCADE)


class UserConnection(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_provider_id = models.ForeignKey(BankProvider, on_delete=models.CASCADE)
    bank_customer_info = models.OneToOneField(BankCustomerInfo, on_delete=models.CASCADE)
    se_customer_id = models.IntegerField()
    se_identifier = models.CharField(max_length=100)
    provider_name = models.CharField(max_length=150)
    se_provider_code = models.CharField(max_length=150)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()
    se_status = models.CharField(max_length=20)
    se_next_refresh_at = models.DateTimeField()
    se_last_success_at = models.DateTimeField()
    se_provider_id = models.IntegerField()
    se_secret = models.CharField(max_length=200)
    se_categorization = models.CharField(max_length=200)
    country_code = models.CharField(max_length=10)


class Account(models.Model):
    id = models.IntegerField(primary_key=True)
    se_account_id = models.IntegerField()
    se_account_name = models.CharField(max_length=100)
    se_currency = models.CharField(max_length=10)
    se_balance = models.IntegerField()
    se_account_nature = models.CharField(max_length=100)
    se_account_holder_name = models.CharField(max_length=100)
    se_available_money = models.IntegerField()
    bank_customer_info_id = models.ForeignKey(BankCustomerInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    se_transaction_id = models.IntegerField()
    se_status = models.CharField(max_length=20)
    se_currency = models.CharField(max_length=10)
    se_transaction_amount = models.IntegerField()
    se_transaction_description = models.CharField(max_length=1000)
    se_transaction_category = models.CharField(max_length=20)
    se_transaction_mode = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
