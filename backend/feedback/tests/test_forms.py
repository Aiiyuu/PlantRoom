from django.test import TestCase
from feedback.models import Feedback
from feedback.forms import FeedbackForm
from account.models import User


class FeedbackFormTest(TestCase):
    """
    Test case to verify the functionality of the Feedback Creation form.

        Tests:
            - Test the validation for the valid data.
            - Test the validation for invalid content length.
            - Test the validation for an invalid rating value.
    """

    def setUp(self):
        # Create a regular User object
        self.user = User.objects.create_user(name='test', email='test@test.com', password='a12a14t56')


    def test_validation_for_valid_data(self):
        """Ensure that no error arises when the data is valid."""

        # Create valid form data
        form = FeedbackForm(data={
            'user': self.user.id,
            'content': 'Lorem ipsum dollar is amet.',
            'rating': 5
        })

        # Assert the form is valid
        self.assertTrue(form.is_valid())


    def test_validation_for_invalid_content_length(self):
        """Ensure that incorrect content length will raise an error."""

        # Create form data with invalid content
        form = FeedbackForm(data={
            'user': self.user.id,
            'content': 'Too short!',  # Content must be greater than 20 characters
            'rating': 5
        })

        # Assert the form is not valid
        self.assertFalse(form.is_valid())

        # Create form data with content that's too long
        form = FeedbackForm(data={
            'user': self.user.id,
            'content': 'Too long!' * 200,  # Content must be less than 800 characters
            'rating': 5
        })

        # Assert the form is not valid
        self.assertFalse(form.is_valid())


    def test_validation_for_invalid_rating_value(self):
        """Ensure that an incorrect rating value will raise an error."""

        # Create form data with an invalid rating (too high)
        form = FeedbackForm(data={
            'user': self.user.id,
            'content': 'Lorem ipsum dollar is amet.',
            'rating': 10  # Rating must be between 0 and 5
        })

        # Assert the form is not valid
        self.assertFalse(form.is_valid())