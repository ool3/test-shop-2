from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, db_index=True, null=True, default='default')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, null=True, default='default')
    image = models.ImageField(upload_to='img', null=True, verbose_name=u'Изображение')
    country = models.CharField(max_length=200, blank=True, null=True)
    price = models.PositiveIntegerField(null=True)
    stock = models.PositiveIntegerField(null=True)
    available = models.BooleanField(default=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    price_multiplier = models.PositiveIntegerField(null=True, default=0)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        unique_together = ('name', 'slug')

    def __str__(self):
        return self.name

class Quantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True)

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.quantity)
        
class Item(models.Model):
    product = models.ManyToManyField(Product)
    quantity = models.IntegerField(default=1, null=True)

        