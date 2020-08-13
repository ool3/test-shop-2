# Generated by Django 3.0.6 on 2020-07-27 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='product',
        ),
        migrations.AddField(
            model_name='item',
            name='product',
            field=models.ManyToManyField(to='products.Product'),
        ),
    ]
