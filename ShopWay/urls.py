"""ShopWay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from carts.views import *
from registration.views import create_user
from django.contrib.auth import views as auth_views
from carts.views import send_order
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('registration/register/', create_user, name='register'),
    path('registration/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('products/carts/', view, name='cart'),
    path('products/carts/all/', send_order, name='send_order'),
    path('products/carts/<slug:slug>/', update_cart, name='update_cart'),
    path('products/carts/<slug:slug>/delete', remove_cart, name='remove_cart'),
    path('products/carts/<slug:slug>/click_value', click_value, name='click_value'),
    
    

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
