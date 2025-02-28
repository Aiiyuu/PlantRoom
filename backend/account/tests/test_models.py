from django.test import TestCase
from account.models import CustomUserManager, User
from django.core.exceptions import ValidationError
from django.utils import timezone


class CustomUserManagerTests(TestCase):
    """
    Test case for verifying the functionalities of creating and managing regular and super users.
    
    - Ensure that a regular user instance is created successfully.
    - Ensure that a super user instance is created successfully.
    - Ensure that creating a user instance without email raises value error.
    """
    
    def test_creating_regular_user(self):
        """Test whether a regular user is created and if the data is saved correctly."""
        
        # Create a user instance
        user = User.objects.create_user(
            name='testuser', 
            email='test@test.com', 
            password='testtest'
        )
        
        
        self.assertEqual(user.name, 'testuser') # Check if the username corresponds with the provided name
        self.assertEqual(user.email, 'test@test.com') # Check if the email corresponds with the provided email
        self.assertTrue(user.check_password('testtest')) # Check if the password corresponds withe the provided
        
        self.assertFalse(user.is_staff) # Ensure that the created user is not staff
        self.assertFalse(user.is_superuser) # Ensure that the created user is not superuser
        
        
    def test_creating_super_user(self):
        """Test whether a superuser is created and if the data is saved correctly."""
        
        
        # Create a superuser instance
        user = User.objects.create_superuser(
            name='admin',
            email='admin@test.com',
            password='admin'
        )
        
        self.assertEqual(user.name, 'admin') # Check if the superuser's name corresponds with the provided name
        self.assertEqual(user.email, 'admin@test.com') # Check if the email corresponds with the provided one
        self.assertTrue(user.check_password('admin')) # Check if the password corresponds with the provided one
        
        self.assertTrue(user.is_staff) # Ensure that the created superuser is staff
        self.assertTrue(user.is_superuser) # Ensure that the created superuser is a superuser
        
        
    def test_creating_user_without_email_raises_value_error(self):
        """Test if the creating a user withoud an email raises a value error."""
        
        with self.assertRaises(ValueError):
            
            # Create a user without an email to ensure that it raises a value error.
            User.objects.create_user(
                name='No email user',
                email=None,
                password='a12a14t56'
            )
            
            

class UserModelTest(TestCase):
    """
    Test case for verifying the functionalities of the User model.
    
    - Ensure that the User objects is correctly displayed in a human-readable way (__str__ method).
    - Ensure that the 'is_regular_user' method works correctly.
    - Ensure that the 'clean' method correctly validatates the user name.
    - Ensure that the 'date_joined' field is set correctly
    """
    
    def setUp(self):
        """Creates or declares assets for the tests."""
        
        # Create a regular user instance for the tests
        self.user = User.objects.create_user(
            name='test_user',
            email='test_user@test.com',
            password='rwqieruqeiouwr'
        )
        
        # Create a superuser instance for the tests
        self.superUser = User.objects.create_superuser(
            name='test_superuser',
            email='admin_superuser@test.com',
            password='qrqwergfgshwwsdg'
        )
    
    def test_user_str_method(self):
        """Ensure that the user instance is displayed by its email."""

        self.assertEqual(str(self.user), self.user.email)
        
    def test_is_regular_user(self):
        """Check if the 'is_regular_user' method returns the expected response."""
        
        self.assertTrue(self.user.is_regular_user()) # It should return true because self.user is a regular user
        self.assertFalse(self.superUser.is_regular_user()) # It should return false
        
    def test_clean_method(self):
        """Test if the 'clean' method correctly validates the user's name."""
        
        # Create a user with the invalid name
        user = User(
            email='_test@test.com',
            name='Jo' # The user's name must have at least 3 characters
        )
        
        # Check if it raises ValidationError
        with self.assertRaises(ValidationError):
            user.clean()
        
        # Change the user's name to a correct one
        user.name='John'
        
        # Check if the clean method does not raise ValidationError
        try:
            user.clean() # It shouldn't raise ValidationError
        except ValidationError:
            self.fail('clean() raised ValidationError unexpectedly!')
            
            
        # Test for leading/trailing spaces being stripped
        user.name = '       John        ' 
        
        user.clean() # It's supposed to strip spaces
        self.assertEqual(user.name, 'John') # The spaces should be stripped
        
    def test_date_joined_is_set_on_user_creation(self):
        """
        Ensure that the user instance include date_joined.
        Ensure that the date time is correct.
        """
        
        # Create a regular user instance
        user = User.objects.create_user(
            name='test__',
            email='test__@test.com',
            password='a12a14t56'
        )
        
        
        # Get the current time to check against
        now = timezone.now()
        
        # Check that the date_joined is not None is a datetime object
        self.assertIsNotNone(user.date_joined)
        self.assertIsInstance(user.date_joined, timezone.datetime)
        
        
        # Check that the date_joined is close to the current time
        # Allow a small margin for creation time
        time_diff = now - user.date_joined
        self.assertLess(time_diff.total_seconds(), 5) # The margin could be up to 5 seconds