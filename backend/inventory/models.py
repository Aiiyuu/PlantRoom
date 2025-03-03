import uuid

from django.db import models
from django.core.exceptions import ValidationError

import os

# Create your models here.


class Plant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # id = models.BigAutoField(primary_key=True)
    
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length='1500', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.PositiveIntegerField(default=0)
    stock_count = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='plants/', blank=False, null=False)
    
    
    class Meta:
        constraints = [
            # Check constraint to ensure price is greater than 0
            models.CheckConstraint(check=models.Q(price__gt=0), name='price_positive'),
            
            # Check constraint to ensure discount percentage is between 0 and 100
            models.CheckConstraint(
                check=models.Q(discount_percentage__gte=0) &
                models.Q(discount_percentage__lte=100),
                name='valid_discount_percentage'
            ),
            
            # Optional: Ensure stock_count is always greater than or equal to 0
            models.CheckConstraint(check=models.Q(stock_count__gte=0), name='valid_stock_count'),
        ]
    
    
    def __str__(self):
        """Return a human-readable string representation of the Plant object."""
        return self.name
    
    
    def get_discounted_price(self):
        """Calculate and return discounted price."""
        
        return self.price - (self.price * self.discount_percentage / 100)
    
    
    @property
    def in_stock(self) -> bool:
        """Return True if the stock_count is greater than 0 or False if it's not."""
        
        return self.stock_count > 0
    
    
    def clean(self):
        """Validates model fields like: name, price, discount_percentage and image"""
        
        self.name = self.name.strip() # Stip leading/traveling spaces from the name field.
        
        # Check if the name field is not empty or fewer than three characters.
        if len(self.name) < 3:
            raise ValidationError('The name cannot be empty or contain fewer than 3 characters.')
        
        # Check if the description is no longer than 1500 characters.
        if self.description and len(self.description) > 1500:
            raise ValidationError('The description field cannot be longer than 1500 characters.')
        
        # Check if the price field is greater than zero.
        if self.price < 0:
            raise ValidationError('The price field must be greater than 0.')
    
        # Check if the discount_percentage is between 0 and 100 (inclusive)
        if not (0 <= self.discount_percentage <= 100):
            raise ValidationError('The discount_percentage field must be within 0 and 100 (inclusive).')
        
        # Check the image format (.png, .jpg or .jpeg)
        valid_image_format = ('.png', '.jpg', '.jpeg') # Create a tuple of allowed formats for the image field
        file_extension = os.path.splitext(self.image.name)[1].lower() # Get the file format of the image
        
        # Check if the file_extension is not in the valid_image_format tuple.
        if file_extension not in valid_image_format:
            raise ValidationError('Only PNG, JPG and JPEG images are allowed.')
        
        # Check the image field size (limit to 10 MB)
        max_size = 10 * 1024 * 1024 # Declare max_size variable for the image field 
    
        # Check if the image field size does not exceed the maximum allowed size
        if self.image.size > max_size:
            raise ValidationError(f'The image field file cannot exceed {max_size / 1024 / 1024}MB.')
    
    
    def save(self, *args, **kwargs):
        """Ensure that the 'clean' method is called before the use instance would be saved."""
        
        self.clean() # Call the 'clean' method
        super().save(*args, **kwargs)
        
        
        