from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about_us/', views.about_as, name='about_as'),
    path('s/', views.search, name='search'),
    path('products/', views.ProductsAll.as_view(), name='products'),
    path('<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path('products/category_all/', views.category_all, name='category_all')
]
