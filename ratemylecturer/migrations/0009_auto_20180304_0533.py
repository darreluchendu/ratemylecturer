# Generated by Django 2.0.1 on 2018-03-04 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratemylecturer', '0008_auto_20180304_0532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addlecturerprofile',
            name='university',
        ),
        migrations.AddField(
            model_name='addlecturerprofile',
            name='bio',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='addlecturerprofile',
            name='picture',
            field=models.ImageField(blank=True, upload_to='profile_images'),
        ),
    ]
