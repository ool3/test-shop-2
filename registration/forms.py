from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class CreateUser(UserCreationForm):
	email = forms.EmailField()
	phone = forms.CharField(max_length=12)
	class Meta:
		model = User
		fields = ('username','phone', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(CreateUser, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['email'].widget.attrs['class'] = 'form-control'
		self.fields['phone'].widget.attrs['class'] = 'form-control'
		self.fields['phone'].widget.attrs['placeholder'] = '+79093035039'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'
