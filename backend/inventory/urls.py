from django.urls import path
from .apis import PlantListAPI, PlantDetailAPI

urlpatterns = [
    path('', PlantListAPI.as_view(), name='plant-list'),
    path('plant/<uuid:id>/', PlantDetailAPI.as_view(), name='plant-detail')
]

