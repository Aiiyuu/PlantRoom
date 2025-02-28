from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone

# Create your models here.


class CustomUserManager(UserManager):
    """
    Custom manager for creating and managing user instance.
    
    This class extands the default 'UserManager' to provide additional methods 
    for creating users and superusers with specific configuration. It includes:
    
    - A method to create regular users with basic configuration.
    - A method to create superusers with the necessary flag sets for admin access.
    - A private method '_create_user' that handles the common logic for user creation. 
    """
    def _create_user(self, name, email, password, **extra_fields):
        """ 
        Check if the email address is provided and convert it to a standard format.
        Create user instance and assign a hashed password to the instance.
        Save the created user instance to the database and return it.

        Raises:
            ValueError: This could raise a validation error if the email adress
            is not provided.

        Returns:
            _type_: Returns the created user instance.
        """
        
        # Check if the email adress is provided
        if not email:
            raise ValueError("You haven't provided a valid email address")
        
        email = self.normalize_email(email) # Convert the email to a standart format
        user = self.model(email=email, name=name, **extra_fields) # Create user
        user.set_password(password) # Assign the hashed pasword to the created user
        user.save(using=self.db) # Save the user instance to the database
        
        return user # Return the instance
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        """
        Creates a regular user and ensures that the necessary fields, like is_staff 
        and is_superuser, are set appropriately for a regular user.
        """
        
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        """
        Creates a superuser(aka: admin) and ensures that the neccessary fields like is_staff
        and is_superuser is set appropriatelly for a superuser
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self._create_user(name, email, password, **extra_fields)
    
    