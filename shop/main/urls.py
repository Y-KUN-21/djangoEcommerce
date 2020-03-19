from django.urls import path, include
from django.shortcuts import render
from .views import (index, detail, HomeView, checkout, DetailProductView, add_to_cart, remove_from_cart, OrderSummary,
                    remove_single_item_from_cart)

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('index/', index, name="index"),
    path('checkout/', checkout, name="checkout"),
    path('product/<slug>', DetailProductView.as_view(), name="product-detail"),
    path('add-to-cart/<slug>', add_to_cart, name="add-to-cart"),
    path('order-summary/', OrderSummary.as_view(), name="order-summary"),
    path('remove-from-cart/<slug>', remove_from_cart, name="remove-from-cart"),
    path('remove-single-item-from-cart/<slug>', remove_single_item_from_cart, name="remove-single-item-from-cart"),
]
