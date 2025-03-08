from rest_framework import serializers
from .models import Feedback
from account.serializers import UserSerializer


class FeedbackSerializer(serializers.ModelSerializer):
    """The FeedbackSerializer serializes data and converts it into a JSON format."""

    user = UserSerializer() # Nested serializer for the 'user' field

    # Create the 'is_current_user' method field
    is_current_user = serializers.SerializerMethodField()

    class Meta:
        model=Feedback
        fields=['id', 'user', 'content', 'rating', 'added_at', 'is_current_user']


    def get_is_current_user(self, obj):
        # Check if the user is authenticated and then compare IDs
        request_user = self.context['request'].user

        if request_user.is_authenticated:
            return obj.user.id == request_user.id  # Compare user IDs
        return False  # For unauthenticated users, return False