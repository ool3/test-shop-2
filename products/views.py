from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView
from .models import Category, Product
from carts.models import Cart
from django.http import HttpResponse, HttpResponseRedirect
import requests
from bs4 import BeautifulSoup as BS
from django.core.paginator import Paginator
# Create your views here.

def home(request):
	# for item in Cart.objects.all():
	# 	print(item.items.product)
	name_button = 'Read more'
	try:
		cart = Cart.objects.filter(user=request.user).last()
		context = cart.products.count()
		category = Category.objects.all()
	except:
		context = None
		category = None
	return render(request, 'shopway/home.html', {'btn_name': name_button, 'total': context, 'category': category})
	



def search(request):
	try:
		q = request.GET.get('q')
	except:
		q = None
	products = Product.objects.filter(name=q)
	if not products:
		products = Product.objects.filter(name__icontains=q.capitalize())
	if not products:
		products = Product.objects.filter(country__icontains=q.capitalize())
	if not products:
		products = Product.objects.filter(country__in=q)
	if not products:
		products = Product.objects.filter(name__icontains=q.capitalize()[:4])
	print(products)

	if not request.user.is_anonymous: 
		cart = Cart.objects.filter(user=request.user).last()
		c = cart.products.count()
		return render(request, 'shopway/search_elements.html', {'products': products, 'q': q, 'total': c})

	else:
		return render(request, 'shopway/search_elements.html', {'products':products, 'q': q})

def get_user(request):
	try:
		cart = Cart.objects.filter(user=request.user).last()
	except:
		cart = None
	return cart

def about_as(request):
	try:
		cart = Cart.objects.filter(user=request.user).last()
		total = cart.products.count()
		all_product = Product.objects.all().count()
	except:
		cart = None
		total = None
		all_product = Product.objects.all().count()
	
	return render(request, 'shopway/about.html', {'total': total, 'all': all_product})

def category_all(request):
	if not request.user.is_anonymous: 
		cart = Cart.objects.filter(user=request.user).last()
		context = cart.products.count()
		return render(request, 'shopway/category_all.html', {'total': context})
	else:
		return render(request, 'shopway/category_all.html')
class ProductsAll(ListView):
	model = Product
	template_name = 'shopway/product_list.html'
	context_object_name = 'products'
	paginate_by = 30

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			context['total'] = get_user(self.request).products.count()
		except:
			pass
		return context

	


class ProductDetail(DetailView):
	model = Product
	context_object_name = 'details'
	template_name = 'shopway/product_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		product = Product.objects.get(slug=self.kwargs['slug'])
		try:
			flag = True
			if product in get_user(self.request).products.all():
				flag = False
			context['cart'] = flag
			context['total'] = get_user(self.request).products.count()
		except:
			pass
		return context