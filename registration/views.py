from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from .forms import CreateUser
def create_user(request):
	if request.method == 'POST':
		form = CreateUser(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('login'))

	else:
		form = CreateUser()
		return render(request, 'registration/register.html', {'form_register': form})