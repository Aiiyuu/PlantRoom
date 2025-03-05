from django.urls import path
from .apis import PlantListAPI

urlpatterns = [
    path('', PlantListAPI.as_view(), name='plant-list'),
]

