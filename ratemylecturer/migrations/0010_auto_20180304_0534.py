# Generated by Django 2.0.1 on 2018-03-04 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratemylecturer', '0009_auto_20180304_0533'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addlecturerprofile',
            old_name='name',
            new_name='bname',
        ),
        migrations.RemoveField(
            model_name='addlecturerprofile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='addlecturerprofile',
            name='picture',
        ),
    ]
