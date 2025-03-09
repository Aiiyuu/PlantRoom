from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Feedback
from account.models import User
from .serializers import FeedbackSerializer
from .forms import FeedbackForm


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


class DeleteFeedbackAPI(APIView):
    """
    The DeleteFeedbackAPI handles a DELETE request to remove
    the Feedback object associated with the provided UUID.
    """

    # Only authenticated users are allowed to access this endpoint
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def delete(self, request, id, *args, **kwargs):
        """
        Check if the Feedback object with the provided id exists.
        Then, check if request.user is the author of the Feedback object,
        and only then delete the Feedback object from the database.
        """

        # Verify whether the Feedback object exists in the database.
        feedback = get_object_or_404(Feedback, id=id)

        # Check if the requested user is the author of the feedback
        if request.user != feedback.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        feedback.delete() # Delete the Feedback object

        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateFeedbackAPI(APIView):
    """
    The CreateFeedbackAPI handles a POST request to
    create a Feedback object.
    """

    # Ony authenticated users are allowed to access this endpoint
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        """Create a Feedback object."""

        # Create a feedback form
        form = FeedbackForm(request.data)

        # Check if the form is valid
        if form.is_valid():
            # Create an instance of the model
            # without saving it to the database
            feedback = form.save(commit=False)

            # Assign the current user to the feedback user field
            feedback.user = request.user
            feedback.save() # Save it to the database

            # Serialize the object to convert it into JSON format
            serializer = FeedbackSerializer(feedback, context={'request': request})

            return Response(serializer.data, status.HTTP_201_CREATED)

        # Return a 400 status code (Bad Request) with the error message.
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)