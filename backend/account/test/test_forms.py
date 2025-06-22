from django.test import TestCase
from account.forms import SignupForm
from account.models import User



class SignupFormTest(TestCase):
    """
    Test the functionalities of the user creation form.
    
    - Test the validation of valid credentials.
    - Test the validation of invalid credentials.
    - Test the validation of unique emails.
    """
    
    
    def test_signup_form_valid(self):
        """Test that the form is valid when correct data is provided."""
        
        # Initialize correct data for the user ceration
        data = {
            'name': 'Ninja',
            'email': 'nja@test.com',
            'password': 'a12a14t56',
            'password1': 'a12a14t56',
            'password2': 'a12a14t56'
        }
        
        # Create a signup form with the correct data
        form = SignupForm(data=data)
        
        self.assertTrue(form.is_valid()) # It should return True
        
    
    def test_signup_form_invalid(self):
        """Test that the form is invalid when incorrect data is provided."""
        
        # Initialize incorect data for the user creation
        data = {
            'name': 'Ninja',
            'email': 'nja@test.com',
            'password': 'a12a14t56',
            'password1': 'a12a14t56',
            'password2': 'qwerty' # Inccorect password confirmation
        }
        
        # Create a signup form with the incorrect data
        form = SignupForm(data=data)
        
        self.assertFalse(form.is_valid()) # The form should be invalid
        self.assertIn('password2', form.errors) # Check if the password2 contains any errors
        
        # Initialize user data with no email provided
        data = {
            'name': 'Ninja',
            'password': 'a12a14t56',
            'password1': 'a12a14t56',
            'password2': 'a12a14t56'
        }
        
        form = SignupForm(data=data) # Create a signup form with an incorrect email
        
        self.assertFalse(form.is_valid()) # The form should be invalid
        self.assertIn('email', form.errors) # Check if the email field contains any errors
        
        
    def test_signup_form_unique_email(self):
        """Check that the form returns an error if the email is already taken."""
        
        # Create a user instance
        User.objects.create_user(
            name='Ninja',
            email='nja@test.com',
            password='a12a14t56'
        )
        
        
        # Initialize user data with an already taken email
        data = {
            'name': 'New Ninja',
            'email': 'nja@test.com',
            'password': 'a12a14t56',
            'password1': 'a12a14t56',
            'password2': 'a12a14t56',
        }
        
        
        form = SignupForm(data=data) # Create a signup form with an already tanke email
        
        self.assertFalse(form.is_valid()) # The form should be invalid
        self.assertIn('email', form.errors) # Ensure that the form has an error for the 'email' field