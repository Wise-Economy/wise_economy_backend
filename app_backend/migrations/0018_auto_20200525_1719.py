# Generated by Django 3.0.6 on 2020-05-25 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_backend', '0017_auto_20200522_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='se_mode',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='se_status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='se_transaction_category',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='se_transaction_mode',
            field=models.CharField(max_length=200),
        ),
    ]
