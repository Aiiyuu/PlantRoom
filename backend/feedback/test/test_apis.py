from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse

from account.models import User
from feedback.models import Feedback

import uuid


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



class DeleteFeedbackAPITest(APITestCase):
    """
    Test case for verifying the functionalities of the DeleteFeedbackAPI endpoint.

    Test:
        - Test successful deletion.
        - Test access restrictions for unauthenticated users.
        - Test the case when the feedback object does not exist in the database.
        - Test the case when the request.user is not the author of the Feedback object.
    """

    def setUp(self):
        """Create test assets for the aforementioned tests."""

        # Initialize the APIClient instance for testing
        self.client = APIClient() # Create a new instance of the APIClient


        # Create two User objects
        self.author = User.objects.create_user(name='test', email='test@test.com', password='a12a14t56')
        self.random_user = User.objects.create_user(name='test', email='test_@test.com', password='a12a14t56')

        # Create a few Feedback objects
        self.feedback1 = Feedback.objects.create(
                                 user=self.author,
                                 content='Great selection of products and fast delivery! Easy shopping experience.',
                                 rating=3
                                 )

        self.feedback2 = Feedback.objects.create(
                                 user=self.author,
                                 content='Smooth checkout process, and my order arrived in perfect condition. Highly recommend!',
                                 rating=2
                                 )

        # Define the URL path for the API endpoint
        self.url = reverse('delete-feedback', kwargs={'id': self.feedback1.id})


    def test_successful_deletion(self):
        """Test successful deletion of the Feedback object."""

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.author)

        # Get the number of Feedback objects for the logged-in user.
        number_of_feedbacks = self.author.feedbacks.all().count()

        # Make a DELETE request to the delete-feedback API endpoint.
        response = self.client.delete(self.url)

        # Assert the status_code is 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Assert that the Feedback object was deleted
        self.assertEqual(self.author.feedbacks.all().count(), number_of_feedbacks - 1)


    def test_access_restriction_for_unauthenticated_users(self):
        """Make sure that unauthenticated users cannot access the delete-feedback API endpoint."""

        # Get the number of Feedback objects in the database.
        number_of_feedbacks = Feedback.objects.all().count()

        # Make a DELETE request to the delete-feedback API endpoint.
        response = self.client.delete(self.url)

        # Assert the status_code is 403 (Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Assert that the Feedback object wasn't deleted
        self.assertEqual(Feedback.objects.all().count(), number_of_feedbacks)


    def test_feedback_does_not_exist(self):
        """Test case for verifying the behavior when no ID is provided."""

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.author)

        # Generate a random UUID not present in the database.
        id = uuid.uuid4()

        # Make a DELETE request to the delete-feedback API endpoint.
        response = self.client.delete(reverse('delete-feedback', kwargs={'id': id}))

        # Assert the status_code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_user_is_not_author_of_feedback(self):
        """
        Test that the Feedback object is not deleted if the request user
        is not the author of the Feedback object associated with the provided ID.
        """

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.random_user)

        # Get the number of Feedback objects in the database
        number_of_feedbacks = Feedback.objects.all().count()

        # Make a DELETE request to the delete-feedback API endpoint.
        response = self.client.delete(self.url)

        # Assert the status_code is 403 (Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Assert that the Feedback object wasn't deleted
        self.assertEqual(Feedback.objects.all().count(), number_of_feedbacks)



class CreateFeedbackAPI(APITestCase):
    """
    Test case for verifying the create-feedback API endpoint.

    Tests:
        - Test access restriction for unauthenticated users.
        - Test the successful creation of a Feedback object.
        - Test the case where a required field is missing.
        - Test the behavior when invalid data is provided.
    """

    def setUp(self):

        # Initialize the APIClient instance for testing
        self.client = APIClient() # Create a new instance of the APIClient

        # Retrieve the URL path to the create-feedback API endpoint.
        self.url = reverse('create-feedback')

        # Create a regular User object
        self.user = User.objects.create_user(name='test', email='test@test.com', password='a12a14t56')


    def test_access_restriction_for_unauthenticated_users(self):
        """Ensure that unauthenticated users cannot access the API endpoint."""

        # Create a data object with the required fields for the Feedback object
        data = {
            'content': 'Lorem ipsum dollar is amet.',
            'rating': 5
        }

        # Make a POST request to the create-feedback API endpoint
        response = self.client.post(self.url, data, format='json')

        # Assert the status code is 403 (Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_successful_feedback_creation(self):
        """
        Ensure that the create-feedback API endpoint returns
        the created Feedback object with a 200 (OK) status code
        after successfully handling the POST request.
        """

        # Login user to avoid access restriction
        self.client.force_authenticate(user=self.user)

        # Create a data object with the required fields for the Feedback object
        data = {
            'content': 'Lorem ipsum dollar is amet.',
            'rating': 5
        }

        # Make a POST request to the create-feedback API endpoint
        response = self.client.post(self.url, data, format='json')

        # Assert the status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the created feedback contains the same field data.
        self.assertEqual(response.data['content'], data['content'])
        self.assertEqual(response.data['rating'], data['rating'])


    def test_missing_required_field_for_feedback_creation(self):
        """Test the behavior when a required field is missing."""

        # Login user to avoid access restriction
        self.client.force_authenticate(user=self.user)

        # Create a data object with the required fields missing.
        # Content field is not provided
        data = {
            'rating': 5
        }

        # Make a POST request to the create-feedback API endpoint
        response = self.client.post(self.url, data, format='json')

        # Assert the status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_invalid_data_is_provided(self):
        """Test the behavior when invalid data is submitted."""

        # Login user to avoid access restriction
        self.client.force_authenticate(user=self.user)

        # Create a data object with invalid field values.
        data = {
            'content': 'Too short!', # it must be between 20 and 800 characters long
            'rating': 10 # It must be between 0 and 5 (inclusive)
        }

        # Make a POST request to the create-feedback API endpoint
        response = self.client.post(self.url, data, format='json')

        # Assert the status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the response contains error messages
        self.assertIn('errors', response.data)

        # Check for content validation error in the __all__ field
        self.assertIn('The content field must include between 20 and 800 characters.', response.data['errors']['__all__'])

        # Check for rating validation error in the __all__ field
        self.assertIn('Constraint “rating_between_0_and_5” is violated.', response.data['errors']['__all__'])