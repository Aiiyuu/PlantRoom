from rest_framework.views import APIView
from rest_framework import status
from .models import User, CustomUserManager
from rest_framework.response import Response
from .forms import SignupForm
from cart.models import Cart


class Signup(APIView):
    """
    Handles the POST request for creating a user instance 
    and saves it to the database if the credentials are valid.
    """
    
    authentication_classes = [] # No authentication is required
    permission_classes = [] # No specific permission checks are enforced
    
    def post(self, request, *args, **kwargs):
        """"
        Create the user's instance and save it to the database if the passed 
        credentials are correct.
        """
        
        # Create an instance of SignupForm using data from the request object.
        form = SignupForm({
            'email': request.data.get('email'),
            'name': request.data.get('name'),
            'password': request.data.get('password1'),
            'password1': request.data.get('password1'),
            'password2': request.data.get('password2')
        })
        
        # Check if the passed credentials are valid to save the instance to the database
        if form.is_valid():
            user = form.save()
            
            # Create an empty Cart object associated with the user.
            Cart.objects.create(user=user)
            
            return Response({'message': 'User was created successfully.'}, status=status.HTTP_201_CREATED)
        
        else:
            errors = [] # Initialize an empty list of errors 
            
            # Iterate through each field in the form
            for field in form:
                # Check if there are any errors for this field
                if field.errors:
                    # Iterate over each error for this field
                    for error in field.errors:
                        # Append each error message to the errors list
                        errors.append(error)
                        
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)