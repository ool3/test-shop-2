# Generated by Django 3.1 on 2020-08-15 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registration', '0006_delete_myuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=122)),
                ('phone', models.CharField(max_length=12)),
            ],
        ),
    ]
