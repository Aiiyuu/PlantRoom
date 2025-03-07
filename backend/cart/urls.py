from django.urls import path
from .apis import CartItemListAPI, AddCartItemAPI, DeleteCartItemAPI, IncreaseQuantityAPI, DecreaseQuantityAPI

urlpatterns = [
    path('', CartItemListAPI.as_view(), name='cart-items-list'),
    path('add/item/', AddCartItemAPI.as_view(), name='add-cart-item'),
    path('remove/item/<uuid:id>/', DeleteCartItemAPI.as_view(), name='delete-cart-item'),
    path('item/increase-quantity/<uuid:id>/', IncreaseQuantityAPI.as_view(), name='increase-cart-item-quantity'),
    path('item/decrease-quantity/<uuid:id>/', DecreaseQuantityAPI.as_view(), name='decrease-cart-item-quantity'),
]