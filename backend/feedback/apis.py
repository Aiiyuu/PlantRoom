from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import Feedback
from account.models import User
from .serializers import FeedbackSerializer


class FeedbackListAPI(APIView):
    """
    The FeedbackListAPI handles a GET request and returns a list of feedback objects.
    """

    permission_classes = [AllowAny] # Allow access to all users.

    def get(self, request, *args, **kwargs):
        """Return a list of Feedback objects."""

        # Fetch all Feedback objects from the database
        feedback_list = Feedback.objects.all()

        # Check if the feedback list is not empty in the database; otherwise, return a 404 response.
        if not feedback_list:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Add the current user to the serializer context
        serializer = FeedbackSerializer(feedback_list, many=True, context={'request': request})

        # Serialize the data to return it as a JSON response.
        return Response(serializer.data, status=status.HTTP_200_OK)