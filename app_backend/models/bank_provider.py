from django.db import models

from app_backend.models.banking import Country


class BankProvider(models.Model):
    id = models.AutoField(primary_key=True)
    se_provider_name = models.CharField(max_length=150)
    se_provider_code = models.CharField(max_length=150)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    se_provider_id = models.IntegerField(null=True)

    @staticmethod
    def create_or_return_bank_provider(connection_data):
        bank_provider = BankProvider.objects.get(se_provider_id=connection_data['provider_id'])
        if bank_provider is None:
            bank_provider = BankProvider(
                se_provider_name=connection_data['provider_name'],
                se_provider_id=connection_data['provider_id'],
                country=Country.objects.get(se_country_code=connection_data['country_code']),
                se_provider_code=connection_data['provider_code'],
            )
        return bank_provider