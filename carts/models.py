from django.db import models
from products.models import Product, Item
from django.contrib.auth.models import User
# Create your models here.

class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	items = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
	products = models.ManyToManyField(Product, blank=True, null=True)
	total = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	available = models.BooleanField(default=False)


	def __str__(self):
		return '{} | {} | {}'.format(self.total, self.user.username, self.user.email)
