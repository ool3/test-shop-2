from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
# Create your views here.
from .models import Cart
from products.models import Product, Category, Quantity
from django.http import HttpResponse, HttpResponseRedirect
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup as BS
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from registration.models import PhoneUser
import time
# Create your views here.


@login_required
def view(request):
	# for x in range(1, 8):
	# 	r = requests.get(f'https://eco-dush.ru/brands/devon-devon/?PAGEN_1={x}&SIZEN_1=180').text
	# 	soup = BS(r, 'html.parser')
	# 	items = soup.find_all('div', class_='col-md-3 product-card')
	# 	counter = 40
	# 	for item in items:
	# 		counter += 1500 * x
	# 		country = item.find('div', class_='products-carousel-el-top').find('span', class_='country').text
	# 		img = 'https://eco-dush.ru/' + item.find('div', class_='products-carousel-el-img').find('img').get('src')
	# 		text = item.find('div', class_='products-carousel-el-title').text.strip()
	# 		price = item.find('span', class_='products-carousel-el-price-1').text.replace(' ', '')
	# 		r = requests.get(img, stream=True)
	# 		name = str(counter) + img.split('/')[-1]
	# 		with open(name, 'bw') as f:
	# 			for chunk in r.iter_content(8192):
	# 				f.write(chunk)
	# 		prod = Product(id=counter, name=text, slug=''.join(('Trustold').lower() + str(counter)), image=name,country=country, price=int(price), stock=1)
	# 		prod.save()

	try:
		a = Cart.objects.get_or_create(user=request.user)
		cart = Cart.objects.filter(user=request.user).last()
		item = cart.products.all()
		all_price = 0
		for i in item:
			all_price += Quantity.objects.filter(user=request.user, product=i).last().quantity
		lol = int(cart.total)

		# Quantity.objects.get_or_create(user=request.user)
		list_q = []
		for i in item:
			q = Quantity.objects.filter(user=request.user, product=i).last()
			print(q)
			list_q.append(q)
			
		q = Quantity.objects.filter(user=request.user)
	except:
		item = None
		all_price = 0
		if not request.user.is_anonymous:
			cart = Cart.objects.filter(user=request.user).last()
			item = cart.products.all()
			all_price = 0
			for i in item:
				all_price += Quantity.objects.filter(user=request.user, product=i).last().quantity
			lol = int(cart.total)
			# Quantity.objects.get_or_create(user=request.user)
			q = Quantity.objects.filter(user=request.user)
			list_q = []
			for i in item:
				q = Quantity.objects.filter(user=request.user, product=i).last()
				print(q)
				list_q.append(q)

		else:
			cart = None
			all_price = 0
			i = None
			lol = None
			list_q = []
	
	return render(request, 'carts/view.html', {'cart': cart.products.all(), 'item_total': lol, 'total': cart.products.all().count(), 'q': list_q})
def send_order(request):
	if request.user.is_superuser:
		if request.method == 'POST':
			if request.POST.get('submit_btn'):
				cart = Cart.objects.filter(available=True, done=False)
			return render(request, 'carts/orders.html', {'cart': cart})
		cart = Cart.objects.filter(available=True, done=False).order_by('-id')
		return render(request, 'carts/orders.html', {'phones': PhoneUser.objects.all(), 'cart': cart})
	else:
		if request.method == 'POST':
			if request.POST.get('submit_btn'):
				cart = Cart.objects.filter(user=request.user).last()
				cart.available = True
				cart.save()
				cart = Cart.objects.filter(user=request.user, available=True).last()
				item = cart.products.all()
				all_price = 0
				
				cart = Cart.objects.filter(user=request.user, available=True)
				Cart.objects.create(user=request.user)
			return render(request, 'carts/orders.html', {'cart': cart, 'all_price': all_price})
		cart = Cart.objects.filter(user=request.user).filter(available=True)
	return render(request, 'carts/orders.html', {'phones': PhoneUser.objects.all(), 'cart': cart})
def done_cart(request, id):
	cart = Cart.objects.filter(id=id).last()
	cart.done = True
	cart.save()
	return HttpResponseRedirect(reverse('send_order'))
@login_required
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
			a = Quantity.objects.create(user=request.user, product=product)
			cart.q.add(Quantity.objects.filter(user=request.user, product=product).last())

		new_total = 0
		for item in cart.products.all():
			new_total += (int(item.price) * int(Quantity.objects.filter(user=request.user, product=item).last().quantity))
		cart.total = new_total
		
		cart.save()
		return HttpResponseRedirect(reverse('home')+ str(slug))
	return HttpResponseRedirect(reverse('register'))
@login_required
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
		cart.q.remove(Quantity.objects.filter(user=request.user, product=product).last())
		new_total = 0

		for item in cart.products.all():
			new_total += (int(item.price) * int(Quantity.objects.filter(user=request.user, product=item).last().quantity))		

		cart.total = new_total
		cart.save()
	return HttpResponseRedirect(reverse('cart'))
def delete_cart(request, id):
	cart = Cart.objects.filter(id=id)
	cart.delete()
	return HttpResponseRedirect(reverse('send_order'))
@login_required
def click_value(request, slug):
	cart = Cart.objects.filter(user=request.user).last()
	new_total = 0
	for item in cart.products.all():
		q = Quantity.objects.filter(user=request.user, product=item).last()
		if request.POST:
			if item.slug == slug:
				if '_up' in request.POST:
					q.quantity += 1
				elif '_down' in request.POST and Quantity.objects.filter(user=request.user, product=item).last().quantity != 1:
					q.quantity -= 1

				q.save()
		new_total += (int(item.price) * int(q.quantity))
	cart.total = new_total
	cart.save()
	return HttpResponseRedirect(reverse('cart'))


def update_price(request):
	# for product in Product.objects.filter(price_multiplier=0):
	# 	product.price_multiplier = product.price / 87.2
	# 	product.save()
	all_prod = []
	for product in Product.objects.all():
		if product.name in all_prod:
			product.delete()
		else:
			all_prod.append(product.name)
	print(all_prod)
	r = requests.get(f'https://yandex.ru/search/?text=курс%20евро&lr=121724&clid=2270455&win=449&src=suggest_B')
	html = BS(r.content, 'html.parser')
	base_page = html.select('.main__center')
	all_current = None
	number_euro = ''
	for page in base_page:
		all_current = page.find('div', class_='content__left').find('ul', class_='serp-list').find_all('div', class_='converter-form__container')
		counter = 0
		for current in all_current:
			if counter != 0:
				number_euro = current.find('span', class_='input').find('span', class_='input__box').find('input').get('value').replace(',', '.')
				print(number_euro)
			counter += 1
	for product in Product.objects.all():
		print(number_euro)
		print(product)
		try:
			product.price = product.price_multiplier * float(number_euro)
			product.save()
		except:
			product.price_multiplier = product.price / float(number_euro)
			product.save()
	return HttpResponseRedirect(reverse('cart'))
