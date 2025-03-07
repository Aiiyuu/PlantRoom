from django.urls import path
from .apis import CartItemListAPI, AddCartItemAPI

urlpatterns = [
    path('', CartItemListAPI.as_view(), name='cart-items-list'),
    path('add/item/', AddCartItemAPI.as_view(), name='add-cart-item')
]