# Generated by Django 2.0.3 on 2018-03-28 01:47

from django.db import migrations, models
import django.utils.timezone
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('ratemylecturer', '0024_auto_20180328_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturerprofile',
            name='picture',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, quality=75, size=[600, 500], upload_to='profile_images'),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='picture',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, quality=75, size=[600, 500], upload_to='profile_images'),
        ),
    ]