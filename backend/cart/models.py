from django.db import models
from account.models import User
from inventory.models import Plant

from django.utils import timezone
import uuid

# Create your models here.


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    
    def __str__(self):
        """Return a human-readable string representation of the Plant object."""
        return self.user.email
    
    
    def get_total(self):
        """Calculates and returns total sum of all items in the cart."""
        
        # Access all cart_items via related_name
        total = sum(item.get_total_price() for item in self.cart_items.all())
        
        return total
    
    def get_items_count(self):
        """Returns the amount of all items in the cart."""

        return self.cart_items.count() # This also uses related_name
        

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateField(default=timezone.now)
    
    
    class Meta:
        constraints = [
            # Check constraint to ensure quantity field is greater then zero.
            models.CheckConstraint(check=models.Q(quantity__gt=0), name='quantity_positive')
        ]
    
    def __str__(self):
        """Return a human-readable string representation of the Plant object."""
        return self.product.name
    
    def get_total_price(self):
        """Calculates and returns total sum of the cart item."""
        
        return self.product.price * self.quantity
    
    def clean(self):
        """Validates model fields like: quantity."""
        
        # Check if the quantity is not negative
        if self.quantity < 0:
            raise ValueError('The quantity field cannot be negative.')
        
        
        # Ensure that a product is only added once to the cart
        # If the product already exists in the cart, update the quantidy instead
        if Cart.objects.filter(cart=self.cart, product=self.product).exists():
            raise ValueError('The product is already in your cart.')
        
    
    def save(self, *args, **kwargs):
        """Ensure that the 'clean' method is called before the instance would be saved."""
        
        self.clean() # Call the clean method
        super().save(*args, *kwargs)
        