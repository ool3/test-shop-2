# Generated by Django 3.1 on 2020-08-14 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20200813_2127'),
        ('carts', '0002_auto_20200814_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='q',
        ),
        migrations.AddField(
            model_name='cart',
            name='q',
            field=models.ManyToManyField(blank=True, null=True, to='products.Quantity'),
        ),
    ]
