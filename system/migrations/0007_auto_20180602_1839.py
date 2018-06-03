# Generated by Django 2.0.2 on 2018-06-02 10:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_auto_20180601_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='shops',
            name='region',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='poll',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 2, 18, 39, 23, 299672)),
        ),
    ]