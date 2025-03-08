from django.test import TestCase
from django.core.exceptions import ValidationError

from feedback.models import Feedback
from account.models import User

import uuid


class FeedbackModelTest(TestCase):
    """
    The FeedbackModelTest test case verifies the functionalities of the Feedback model.

    Tests:
        - Test the object creation.
        - Test that the UUID is generated automatically.
        - Test that the UUID is unique.
        - Test that the UUID consistent on save.
        - Test that the content leading & trailing spaces are stripped.
        - Test the content field invalid length.
        - Test the handling of invalid values for the rating field.
        - Test the related_name for the user field.
        - Test that the __str__ method represents the object correctly.
        - Test the feedback deletion on user deletion.
    """

    def setUp(self):

        # Create a regular User object
        self.user = User.objects.create_user(name='test', email='test@test.com', password='a12a14t56')

        # Create a few Feedback objects
        self.feedback1 = Feedback.objects.create(
                            user = self.user,
                            rating = 5,
                            content = 'Great job on the project! Your effort and attention to detail really showed.'
                        )

        self.feedback2 = Feedback.objects.create(
                            user = self.user,
                            rating = 4,
                            content = 'Nice work on the presentation! Clear, concise, and well-organized. Keep it up!'
                        )


    def test_uuid_is_generated_automatically(self):
        """
        Test that a UUID is generated correctly when a Feedback
        object is saved to the database.
        """

        # Create a new Feedback object
        feedback = Feedback.objects.create(
                        user = self.user,
                        rating = 5,
                        content = 'Lorem ipsum dollar is amet.'
                    )

        self.assertIsInstance(feedback.id, uuid.UUID) # Check if the id of type UUID
        self.assertIsNotNone(feedback.id) # Ensure that the id field is not None


    def test_uuids_are_unique(self):
        """Ensure that Feedback objects have different UUIDs."""

        # Ensure that the UUIDs of two Feedback objects are not the same
        self.assertNotEqual(self.feedback1.id, self.feedback2.id)


    def test_uuid_consistency_on_save(self):
        """Ensure that the UUID does not change after saving the object again."""

        initial_id = self.feedback1.id # Get the object id before saving it

        self.feedback1.save() # Save the Feedback object

        self.assertEqual(initial_id, self.feedback1.id) # Ensure that the id field remains unchanged


    def test_content_stripping_spaces(self):
        """Make sure that the 'clean' method removes leading/trailing spaces from the content field."""

        # Create a new Feedback object
        feedback = Feedback.objects.create(
                       user = self.user,
                       rating = 5,
                       content = '         Lorem ipsum dollar is amet.     '
                   )


        # Assert the spaces were removed
        self.assertEqual(feedback.content, 'Lorem ipsum dollar is amet.')


    def test_invalid_length_of_content_field(self):
        """
        Test that a Feedback object cannot be saved in the database if the
        content length is less than 20 or greater than 800 characters.
        """

        # Declare a too short Feedback object
        feedback = Feedback(
                           user=self.user,
                           content='Too short!',
                           rating=5
                           )

        # Assert the object cannot be saved to the database
        with self.assertRaises(ValidationError):
            feedback.save() # It should raise a ValidationError


        # Make the content of the Feedback object too long.
        feedback.content = 'long' * 201 # It will be 804 characters long.

        # Assert the object cannot be saved to the database
        with self.assertRaises(ValidationError):
             feedback.save() # It should raise a ValidationError


    def test_handling_invalid_rating_field(self):
        """
        Ensure that a Feedback object cannot be saved to the database
        if its value is not between 0 and 5 (inclusive).
        """

        # Declare a Feedback object with incorrect rating value
        feedback = Feedback(
                        user=self.user,
                        content='Lorem ipsum dollar is amet.',
                        rating=7 # It must not be greater than 5
                    )

        # Assert the object cannot be saved to the database
        with self.assertRaises(ValidationError):
             feedback.save() # It should raise a ValidationError


    def test_user_field_related_name(self):
        """Test the behavior of the related_name in the user field."""

        # Ensure that you can access the Feedback objects from the User instance.
        self.assertTrue(self.user.feedbacks.all())


    def test_feedback_str_method(self):
        """
        Ensure that the __str__ method returns a string representation
        of the Feedback object.
        """

        # Ensure that the __str___ method returns the first 20 characters
        # of the content field, after stripping any leading or trailing whitespace
        self.assertEqual(str(self.feedback1), self.feedback1.content[:20].strip())


    def test_feedback_deletion_on_user_deletion(self):
        """Test that the Feedback object is deleted when the associated User object is deleted."""

        # Firstly, assert that the user's feedback exists.
        self.assertTrue(self.user.feedbacks.all().exists())
        feedback_id = self.feedback1.id # Get the Feedback ID before deleting the user

        self.user.delete() # Delete the User object

        # Ensure that the feedback object does not exist in the database
        self.assertFalse(Feedback.objects.filter(id=feedback_id).exists())