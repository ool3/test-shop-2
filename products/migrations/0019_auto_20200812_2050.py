# Generated by Django 3.1 on 2020-08-12 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='img', verbose_name='Изображение'),
        ),
    ]
