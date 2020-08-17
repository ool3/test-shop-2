# Generated by Django 3.1 on 2020-08-14 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20200813_2127'),
        ('carts', '0005_cart_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='q',
        ),
        migrations.AddField(
            model_name='cart',
            name='q',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.quantity'),
        ),
    ]