from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from account.models import User


class SignupAPIViewTest(APITestCase):
    """
    Test the behavior and functionality of the Signup api view.
    
    - Test successful user creation with valid data.
    - Test unsuccessful user creation with invalid data.
        - Invalid email formats.
        - Mismatched passwords.
        - Missing required fields.
        - The password field is too weak
    - Test proper error handling when the email already exist.
    - Ensuring the correct status codes and response messages.
    """
    
    def test_signup_success(self):
        """Test that the API creates a user successfully with valid data."""
        
        # Create valid data for the user object
        data = {
            'name': 'testuser',
            'email': 'test@test.com',
            'password1': 'strongpassword123123',
            'password2': 'strongpassword123123',
        }
        
        # Make a POST request to the signup API, passing the valid data for user object creation in JSON format.
        response = self.client.post(reverse('signup'), data, format='json')
        
        # Assert that the correct status code is returned
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
        # Ensure that the created user object exists in the database.
        self.assertTrue(User.objects.filter(email='test@test.com').exists())
        
        
    def test_signup_invalid_email_format(self):
        """Test the API behavior when passing an incorrect email format."""
        
        # Create data with an invalid email format for user creation.
        data = {
            'name': 'testuser',
            'email': 'invalidemail.com',
            'password1': 'strongpassword123123',
            'password2': 'strongpassword123123'
        }
        
        # Make a POST request to the signup API, passing an incorrect email.
        response = self.client.post(reverse('signup'), data, format='json')
        
        # Assert that the status code is equal to 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Ensure that the email field contains any forms error
        self.assertIn('email', response.data['errors'][0])
        
        
    def test_signup_password_mismatch(self):
        """Ensure that the signup API correctly handles mismatched passwords situation."""
        
        # Create data with mismatched passwords for user creation
        data = {
            'name': 'testuser',
            'email': 'test@test.com',
            'password1': 'strongpassword123',
            'password2': 'differentpassword123',
        }
        
        
        # Make a POST request to the API, passing mismatched passwords
        response = self.client.post(reverse('signup'), data, format='json')
        
        
        # Check that the API returns a 400 status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Check that the password field contains any errors
        self.assertIn('password', response.data['errors'][0])
        
        
    def test_signup_missing_fields(self):
        """Test that the API correctly handles missing fields"""
        
        # Create data with missing name field, which is required
        data = {
            'email': 'test@test.com',
            'password1': 'strongpassword123123',
            'password2': 'strongpassword123123'
        }
        
        
        # Make a POST request to the API, passing data with missing 'name' field
        response = self.client.post(reverse('signup'), data, format='json')
        
        
        # Verify that the API returns a 400 status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Ensure that the API returns an error message 'This field is required'
        self.assertEqual(response.data['errors'][0], 'This field is required.')
        
    
    def test_signup_duplicate_email(self):
        """Test the API's behavior if the email is already taken"""
        
        
        # Create a user object
        User.objects.create_user(
            name='testuser',
            email='existingemail@test.com',
            password='strongpassword123123'
        )
        
        # Create data with already taken user email
        data = {
            'name': 'testuser',
            'email': 'existingemail@test/.com',
            'password1': 'strongpassword123123',
            'password2': 'strongpassword123123'
        }
        
        
        # Make a POST request to the API, passing an already taken user email
        response = self.client.post(reverse('signup'), data, format='json')
        
        # Verify that the API returns a 400 status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Check that the email field contains errors
        self.assertIn('email', response.data['errors'][0])
        
        
    def test_signup_weak_password(self):
        """Test that the API returns an error when a weak password is provided"""
        
        
        # Create data with weak passwords
        data = {
            'name': 'testuser',
            'email': 'test@test.com',
            'password1': '123',
            'password2': '123',
        }
        
        
        # Make a POST request to the API, passing too weak password
        response = self.client.post(reverse('signup'), data, format='json')
        
        # Check that the API returns a 400 status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify that the password field contains errors
        self.assertIn('This password is too short. It must contain at least 8 characters.', response.data['errors'])