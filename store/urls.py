"""Tshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from .views import home,cart,login,orders,signup,checkout,signout,show_product,add_to_cart,validatePayment

urlpatterns = [
    path('', home, name='home'),
    path('cart', cart, name='cart'),
    path('login', login, name='login'),
    path('orders', orders, name='orders'),
    path('signup', signup, name='signup'),
    path('logout', signout, name='signout'),
    path('checkout', checkout, name='checkout'),
    path('product/<str:slug>', show_product, name='show_product'),
    path('addtocart/<str:slug>/<str:size>', add_to_cart, name='add_to_cart'),
    path('validate_payment', validatePayment, name='validatepayment'),
    

]
