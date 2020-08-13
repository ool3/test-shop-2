from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from carts.models import Cart
class CreateUser(UserCreationForm):
	email = forms.EmailField()
	phone = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'placeholder': '89063049828'}))
	
	class Meta:
		model = User
		fields = ('username','phone', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(CreateUser, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['email'].widget.attrs['class'] = 'form-control'
		self.fields['phone'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'placeholder': '89063049828'}))

	class Meta:
		model = User
		fields = ('username', 'phone', 'email')

	def __init__(self, *args, **kwargs):
		super(UserUpdateForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['email'].widget.attrs['class'] = 'form-control'
