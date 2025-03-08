from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse

from account.models import User
from feedback.models import Feedback



class FeedbackListAPITest(APITestCase):
    """
    Test case for verifying the functionalities of the FeedbackListAPI endpoint.

    Tests:
        - Ensure that unauthenticated users can access the API endpoint.
        - Ensure that authenticated users can access the API endpoint.
        - Test successful handling of the GET request.
        - Test the behavior when Feedback objects do not exist in the database.
        - Test the 'is_current_user' field for another user.
    """

    def setUp(self):
        """Create the necessary assets for the tests written above."""

        # Initialize the APIClient instance for testing
        self.client = APIClient() # Create a new instance of the APIClient

        self.url = reverse('feedback-list') # Define the API endpoint.

        # Create regular user and superuser objects
        self.regular_user = User.objects.create_user(name='regular_user', email='test@test.com', password='a12a14t56')
        self.superuser = User.objects.create_superuser(name='superuser', email='test_@test.com', password='a12a14t56')


        # Create a few Feedback objects
        self.feedback1 = Feedback.objects.create(
                                 user=self.regular_user,
                                 content='Great selection of products and fast delivery! Easy shopping experience.',
                                 rating=3
                                 )

        self.feedback2 = Feedback.objects.create(
                                 user=self.regular_user,
                                 content='Smooth checkout process, and my order arrived in perfect condition. Highly recommend!',
                                 rating=2
                                 )


        self.feedback3 = Feedback.objects.create(
                                 user=self.regular_user,
                                 content='The website is user-friendly, and my items came on time. I\'ll definitely shop again.',
                                 rating=5
                                 )

        self.feedback4 = Feedback.objects.create(
                                 user=self.regular_user,
                                 content='Impressive quality and quick service. I’m happy with my purchase and the overall experience.',
                                 rating=4
                                 )


    def test_access_for_unauthenticated_user(self):
        """Ensure that unauthenticated users can access the Feedback objects from the database."""

        # Make a GET request to the feedback-list API endpoint
        response = self.client.get(self.url)

        # Assert the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_access_for_authenticated_user(self):
        """Ensure that authenticated users can access the Feedback objects."""

        # Authenticate the user
        self.client.force_authenticate(user=self.regular_user)

        # Make a GET request to the feedback-list API endpoint
        response = self.client.get(self.url)

        # Assert the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_successful_handling(self):
        """Test that the received data from the database is correct."""

        # Authenticate the user
        self.client.force_authenticate(user=self.regular_user)

        # Make a GET request to the feedback-list API endpoint
        response = self.client.get(self.url)

        # Ensure that the response contains the feedback data
        self.assertIn('id', response.data[0])  # Check that 'id' exists in the first feedback entry
        self.assertIn('user', response.data[0])  # Check that 'user' exists in the first feedback entry
        self.assertIn('content', response.data[0])  # Check that 'content' exists
        self.assertIn('rating', response.data[0])  # Check that 'rating' exists
        self.assertIn('added_at', response.data[0])  # Check that 'added_at' exists
        self.assertIn('is_current_user', response.data[0])  # Check that 'is_current_user' exists

        # Assert the value of 'is_current_user' based on the authenticated user
        feedback_data = response.data[0]
        self.assertTrue(feedback_data['is_current_user'])  # Since the feedback user matches the regular_user


    def test_is_current_user_false_for_another_user(self):
            """Test that 'is_current_user' is False when the feedback is by another user."""

            # Authenticate with a different user
            self.client.force_authenticate(user=self.superuser)

            # Make a GET request to the feedback-list API endpoint
            response = self.client.get(self.url)

            # Ensure that 'is_current_user' is False since the superuser is not the creator of the feedback
            feedback_data = response.data[0]

            # Should be False because the superuser isn't the feedback owner
            self.assertFalse(feedback_data['is_current_user'])


    def test_feedbacks_do_not_exist(self):
        """
        Verify the behavior of the feedback-list API endpoint when
        Feedback objects do not exist in the database.
        """

        # Make sure that Feedback objects do not exist in the database
        Feedback.objects.all().delete() # Delete all objects from the database

        # Make a GET request to the feedback-list API endpoint
        response = self.client.get(self.url)

        # Assert the status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)