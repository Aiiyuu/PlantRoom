from django.contrib.auth.forms import UserCreationForm
from .models import User 


class SignupForm(UserCreationForm):
    """
    SignupForm is a custom form the extend from the built-in UserCreationForm
    to handle user registration. It uses the custom User model for the application.
    
    Attributes:
        - name: 
        - email: 
        - password: The password chosen by the user.
    """
    
    class Meta:
        model = User
        fields = ['name', 'email', 'password']