# Generated by Django 3.0.6 on 2020-07-13 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_backend', '0024_auto_20200617_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='currency_symbol',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='isd_code',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]
