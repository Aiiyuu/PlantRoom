from django.urls import path
from .apis import FeedbackListAPI

urlpatterns = [
    path('', FeedbackListAPI.as_view(), name='feedback-list'),
]