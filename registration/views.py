from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from .forms import CreateUser
from .models import PhoneUser
def create_user(request):
	if request.method == 'POST':
		print(request.POST)
		form = CreateUser(request.POST)
		if form.is_valid():
			PhoneUser.objects.create(username=request.POST['username'], phone=request.POST['phone'])
			form.save()
			return HttpResponseRedirect(reverse('login'))

	else:
		form = CreateUser()
	return render(request, 'registration/register.html', {'form_register': form})