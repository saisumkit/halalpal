# Generated by Django 2.0.2 on 2018-05-30 15:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(choices=[('F', 'Favorite')], max_length=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200)),
                ('expiry_date', models.DateTimeField(default=datetime.datetime(2018, 5, 30, 23, 49, 28, 812700))),
                ('no_of_participant', models.IntegerField(default=2)),
                ('current_participant', models.IntegerField(default=0)),
                ('code', models.CharField(max_length=200)),
                ('closed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=250)),
                ('body', models.TextField(default='')),
                ('rating', models.IntegerField(default=5)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shops',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=1000)),
                ('address', models.CharField(max_length=1024)),
                ('location', models.CharField(max_length=1024)),
                ('postal_code', models.CharField(max_length=10)),
                ('website', models.CharField(max_length=1000)),
                ('facebook', models.CharField(max_length=1000)),
                ('instagram', models.CharField(max_length=1000)),
                ('phone_number', models.CharField(max_length=1000)),
                ('email', models.CharField(max_length=1000)),
                ('number_of_people_rated', models.IntegerField(default=0)),
                ('current_rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Poll')),
                ('selected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Choice')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_set', to='system.Shops'),
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Poll'),
        ),
        migrations.AddField(
            model_name='choice',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Shops'),
        ),
    ]
