from django.urls import path
from .apis import CartItemListAPI, AddCartItemAPI, DeleteCartItemAPI

urlpatterns = [
    path('', CartItemListAPI.as_view(), name='cart-items-list'),
    path('add/item/', AddCartItemAPI.as_view(), name='add-cart-item'),
    path('remove/item/', DeleteCartItemAPI.as_view(), name='delete-cart-item'),
]