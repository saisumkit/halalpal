# Generated by Django 2.1 on 2018-10-23 23:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_auto_20180603_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='poll',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 24, 7, 5, 33, 399082)),
        ),
    ]
