# Generated by Django 3.0.6 on 2020-05-21 13:07

import app_backend.models.user_connection
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_backend', '0009_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userconnection',
            name='se_conn_session_status',
            field=models.CharField(default=app_backend.models.user_connection.SaltEdgeConnectSessionStatus['DEFAULT'], max_length=20),
        ),
    ]
