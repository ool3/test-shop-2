# Generated by Django 3.1 on 2020-08-15 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_myuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]
