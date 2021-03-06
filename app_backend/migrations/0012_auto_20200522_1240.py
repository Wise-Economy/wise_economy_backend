# Generated by Django 3.0.6 on 2020-05-22 12:40

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_backend', '0011_auto_20200521_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='balance_snapshot',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='payee_info',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='se_made_on',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='se_mode',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='se_status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='se_transaction_description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
