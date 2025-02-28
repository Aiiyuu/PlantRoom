from django.test import TestCase
from account.models import CustomUserManager, User


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