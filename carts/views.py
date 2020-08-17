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
# Create your views here.


@login_required
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
	try:
		# session = requests.Session()
		# retry = Retry(connect=3, backoff_factor=0.5)
		# adapter = HTTPAdapter(max_retries=retry)
		# session.mount('http://', adapter)
		# session.mount('https://', adapter)

		# session.get(url)
		username = 'kefjfhjsf'
		token = '1c4ea174d54d1362538bfe9e9ee9d78f406d6d54'

		response = requests.get(
		'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(
			username=username
		),
		headers={'Authorization': 'Token {token}'.format(token=token)}
		)
		if response.status_code == 200:
			print('CPU quota info:')
			print(response.content)
		else:
			print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))		
		r = requests.get(f'https://cbr.ru/')
		html = BS(r.content, 'html.parser')
		base_page = html.select('.row.flex-nowrap.home-indicators_items')
		for page in base_page:
			page_block = page.select('.indicator_el.indicator_course')
		counter = 0
		for block in page_block:
			if counter == 1:
				euro = [i.text[:-1] for i in block.select('.indicator_el_value.mono-num')]
				number_euro = float(euro[-1].replace(',', '.'))
			counter += 1
		for product in Product.objects.all():
			product.price = product.price_multiplier * number_euro
			product.save()
	except requests.exceptions.ConnectionError:
		r = requests.get(f'https://cbr.ru/')
		r.status_code = "Connection refused"
	return HttpResponseRedirect(reverse('cart'))
