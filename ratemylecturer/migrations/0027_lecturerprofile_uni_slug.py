# Generated by Django 2.0.3 on 2018-03-28 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratemylecturer', '0026_merge_20180328_0630'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturerprofile',
            name='uni_slug',
            field=models.CharField(default='djangodbmodelsfieldscharfield', max_length=30),
        ),
    ]