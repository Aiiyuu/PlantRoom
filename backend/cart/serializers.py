from rest_framework import serializers
from .models import CartItem
from inventory.serializers import PlantSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """
    The CartItemSerializer serializes data and converts it into JSON format.
    """
    
    # Define a custom field to calculate total price
    total_price = serializers.SerializerMethodField()
    product = PlantSerializer() # Nested serializer for 'product' field
    
    class Meta:
        model=CartItem
        fields=['id', 'product', 'quantity', 'added_at', 'total_price']
        
    def get_total_price(self, obj):
        """Custom method to calculate the total price of the cart item."""
        return obj.get_total_price()