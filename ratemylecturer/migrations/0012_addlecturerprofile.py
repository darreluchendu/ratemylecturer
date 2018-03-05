# Generated by Django 2.0.1 on 2018-03-04 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratemylecturer', '0011_delete_addlecturerprofile'),
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
    ]