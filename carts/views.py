from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
# Create your views here.
from .models import Cart
from products.models import Product, Category
from django.http import HttpResponse, HttpResponseRedirect
import requests
from bs4 import BeautifulSoup as BS
from django.contrib.auth.models import User
# Create your views here.
def view(request):
	# for x in range(1, 14):
	# 	r = requests.get(f'https://eco-dush.ru/brands/armani-roca/?PAGEN_1={x}&SIZEN_1=36').text
	# 	soup = BS(r, 'lxml')
	# 	items = soup.find_all('div', class_='col-md-3 product-card')
	# 	counter = 5
	# 	for item in items:
	# 		counter += 4 * x
	# 		country = item.find('div', class_='products-carousel-el-top').find('span', class_='country').text
	# 		img = 'https://eco-dush.ru/' + item.find('div', class_='products-carousel-el-img').find('img').get('src')
	# 		text = item.find('div', class_='products-carousel-el-title').text.strip()
	# 		price = item.find('span', class_='products-carousel-el-price-1').text.replace(' ', '')
	# 		r = requests.get(img, stream=True)
	# 		name = str(counter) + img.split('/')[-1]
	# 		with open(name, 'bw') as f:
	# 			for chunk in r.iter_content(8192):
	# 				f.write(chunk)
	# 		prod = Product(id=counter, name=text, slug='-'.join(('a').lower() + str(counter)), image=name,country=country, price=int(price), stock=1)
	# 		prod.save()

	try:
		a = Cart.objects.get_or_create(user=request.user)
		cart = Cart.objects.filter(user=request.user).last()
		item = cart.products.count()
		i = int(cart.total)
	except:
		item = None
		if not request.user.is_anonymous:
			cart = Cart.objects.filter(user=request.user).last()
			i = int(cart.total)
		else:
			cart = None
			i = None
	
	return render(request, 'carts/view.html', {'cart': cart, 'item_total': item, 'total': i})

def send_order(request):
	if request.user.is_superuser:
		if request.method == 'POST':
			if request.POST.get('submit_btn'):
				cart = Cart.objects.filter(available=True)
			return render(request, 'carts/orders.html', {'cart': cart})
		cart = Cart.objects.filter(available=True)
		return render(request, 'carts/orders.html', {'cart': cart})
	else:
		if request.method == 'POST':
			if request.POST.get('submit_btn'):
				cart = Cart.objects.filter(user=request.user).last()
				cart.available = True
				cart.save()
				cart = Cart.objects.filter(user=request.user).filter(available=True)
				Cart.objects.create(user=request.user)
			return render(request, 'carts/orders.html', {'cart': cart})
		cart = Cart.objects.filter(user=request.user).filter(available=True)
	return render(request, 'carts/orders.html', {'cart': cart})

def update_cart(request, slug):
	if not request.user.is_anonymous:
		cart = Cart.objects.filter(user=request.user).last()
		try:
			product = Product.objects.get(slug=slug)
		except Product.DoesNotExist:
			pass
		except:
			pass
		if product not in cart.products.all():
			cart.available = False
			cart.products.add(product)

		new_total = 0
		for item in cart.products.all():
			new_total += (int(item.price) * int(item.quantity))
		
		cart.total = new_total
		
		cart.save()
	return HttpResponseRedirect(reverse('home')+ str(slug))

def remove_cart(request, slug):
	cart = Cart.objects.filter(user=request.user).last()
	try:
		product = Product.objects.get(slug=slug)
	except Product.DoesNotExist:
		pass
	except:
		pass
	if product in cart.products.all():
		cart.products.remove(product)
		new_total = 0
		for item in cart.products.all():
			new_total += (int(item.price) * int(item.quantity))		
		cart.total = new_total
		cart.save()
	return HttpResponseRedirect(reverse('cart'))

def click_value(request, slug):
	cart = Cart.objects.filter(user=request.user).last()
	new_total = 0
	for item in cart.products.all():
		if request.POST:
			if item.slug == slug:
				if '_up' in request.POST:
					print(item)
					item.quantity += 1
				elif '_down' in request.POST and item.quantity != 1:
					item.quantity -= 1
		item.save()
		new_total += (int(item.price) * int(item.quantity))
	cart.total = new_total
	cart.save()
	return HttpResponseRedirect(reverse('cart'))