# Generated by Django 3.0.6 on 2020-05-21 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_backend', '0008_auto_20200521_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('se_transaction_id', models.IntegerField()),
                ('se_status', models.CharField(max_length=20)),
                ('se_currency', models.CharField(max_length=10)),
                ('se_transaction_amount', models.IntegerField()),
                ('se_transaction_description', models.CharField(max_length=1000)),
                ('se_transaction_category', models.CharField(max_length=20)),
                ('se_transaction_mode', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_backend.Account')),
            ],
        ),
    ]
