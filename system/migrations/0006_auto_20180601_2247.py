# Generated by Django 2.0.2 on 2018-06-01 14:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_auto_20180601_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='shops',
            name='categorization',
            field=models.CharField(default='others', max_length=256),
        ),
        migrations.AlterField(
            model_name='poll',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 1, 22, 47, 47, 121192)),
        ),
    ]
