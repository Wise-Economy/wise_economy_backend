# Generated by Django 3.0.6 on 2020-05-22 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_backend', '0016_auto_20200522_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='se_transaction_id',
            field=models.CharField(max_length=100),
        ),
    ]