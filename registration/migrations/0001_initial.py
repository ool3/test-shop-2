# Generated by Django 3.1 on 2020-08-14 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=8)),
                ('email', models.EmailField(max_length=120)),
                ('password1', models.CharField(max_length=120)),
                ('password2', models.CharField(max_length=120)),
            ],
        ),
    ]
