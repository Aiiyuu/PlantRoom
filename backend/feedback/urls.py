from django.urls import path
from .apis import FeedbackListAPI, DeleteFeedbackAPI, CreateFeedbackAPI

urlpatterns = [
    path('', FeedbackListAPI.as_view(), name='feedback-list'),
    path('delete/<uuid:id>/', DeleteFeedbackAPI.as_view(), name='delete-feedback'),
    path('create/', CreateFeedbackAPI.as_view(), name='create-feedback')
]