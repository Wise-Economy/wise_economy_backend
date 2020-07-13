from django.db import models

from app_backend.models.country import Country


class BankProvider(models.Model):
    id = models.AutoField(primary_key=True)
    se_provider_name = models.CharField(max_length=150)
    se_provider_code = models.CharField(max_length=150)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    se_provider_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    icon_url = models.CharField(max_length=2048, default=None, blank=True, null=True)

    @staticmethod
    def create_or_return_bank_provider(connection_data, country):
        bank_provider = BankProvider.objects.filter(se_provider_id=connection_data['provider_id']).first()
        if bank_provider is None:
            bank_provider = BankProvider.objects.create(
                se_provider_name=connection_data['provider_name'],
                se_provider_id=connection_data['provider_id'],
                country=country,
                se_provider_code=connection_data['provider_code'],
            )
        return bank_provider
