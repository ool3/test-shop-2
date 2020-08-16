from django.contrib import admin
from .models import Category, Product,Quantity


class CategoryAdmin(admin.ModelAdmin):
	search_fields = ['name', 'slug'] # search 
	list_display = ['name', 'slug'] # dislpay
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
	date_hierarchy = 'created'
	# readonly_fileds = ['updated', 'updated']
	search_fields = ['name', 'slug', 'price']
	list_display = ['name', 'slug', 'price', 'stock', 'available', 'country']
	list_filter = ['available', 'country'] # filter components
	list_editable = ['price','slug', 'stock', 'available'] # edit
	prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)
admin.site.register(Quantity)