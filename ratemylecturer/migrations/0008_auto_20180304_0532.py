# Generated by Django 2.0.1 on 2018-03-04 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratemylecturer', '0007_auto_20180304_0531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addlecturerprofile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='addlecturerprofile',
            name='department',
        ),
        migrations.RemoveField(
            model_name='addlecturerprofile',
            name='picture',
        ),
    ]
