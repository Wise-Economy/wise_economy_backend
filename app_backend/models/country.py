from django.db import models


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=100)
    currency_name = models.CharField(max_length=100)
    currency_code = models.CharField(max_length=20)
    se_country_id = models.IntegerField(default=None, blank=True, null=True)
    se_country_code = models.CharField(max_length=10)
    country_flag_icon_url = models.CharField(max_length=2048, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    isd_code = models.CharField(max_length=10, default=None, blank=True, null=True)
    currency_symbol = models.CharField(max_length=10, default=None, blank=True, null=True)

    ENABLED_COUNTRIES = ['Germany', 'United Kingdom']

    @staticmethod
    def get_enabled_countries():
        return Country.objects.filter(country_name__in=Country.ENABLED_COUNTRIES)

