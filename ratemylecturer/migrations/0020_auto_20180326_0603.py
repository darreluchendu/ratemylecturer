# Generated by Django 2.0.3 on 2018-03-26 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratemylecturer', '0019_auto_20180323_0429'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturerprofile',
            name='picture_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='picture_url',
            field=models.URLField(blank=True),
        ),
    ]
