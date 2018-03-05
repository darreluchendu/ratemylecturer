# Generated by Django 2.0.1 on 2018-03-04 05:31

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_supervisedregistrationprofile'),
        ('admin', '0002_logentry_remove_auto_add'),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('ratemylecturer', '0006_usermethods'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddLecturerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('university', models.CharField(max_length=30)),
                ('department', models.CharField(max_length=30)),
                ('bio', models.CharField(blank=True, max_length=200)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
            ],
        ),
        # migrations.RemoveField(
        #     model_name='usermethods',
        #     name='user_ptr',
        # ),
        migrations.DeleteModel(
            name='UserMethods',
        ),
        migrations.CreateModel(
            name='UserMethods',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]