from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    """
    FeedbackForm is a ModelForm for the Feedback model. It handles the creation
    and validation of Feedback objects, including fields for user, content,
    rating, and added_at.

    Attributes:
        - user: The user giving the feedback.
        - content: The feedback content (max 800 characters).
        - rating: A positive integer for the user's rating.
    """

    class Meta:
        model = Feedback
        fields = ['user', 'content', 'rating']