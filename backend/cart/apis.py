from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Cart, CartItem
from inventory.models import Plant
from .serializers import CartItemSerializer


class CartItemListAPI(APIView):
    """
    The CartItemListAPI handles a GET request and returns a list of cart 
    items associated with the user object.
    
    This API endpoint allows authenticated users to retrieve a list of cart items, 
    including the plant, quantity, and total sum.
    """
    
    # Restrict access to unauthenticated users
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """Handles a GET request to fetch and return a list of plants added to the cart."""
        
        # Retrieve the Cart object from the database, or return a 404 if it is not found.
        cart = get_object_or_404(Cart, user=request.user)
        
        
        # Check if the cart is not empty
        if not cart.cart_items.all().count():
            return Response({'message': 'Your cart is empty.'}, status=status.HTTP_200_OK)
        
        # Serializer the cart items using the CartItemSerializer
        serializer = CartItemSerializer(cart.cart_items.all(), many=True)
        
        # Data that will be returned and displayed on a web page. 
        context = {
            'items': serializer.data,
            'total_cart_price': cart.get_total(),
            'total_items_count': cart.get_items_count()
        }
        
        return Response(context, status=status.HTTP_200_OK)
    
    
class AddCartItemAPI(APIView):
    """
    The AddCartItemAPI handles a POST request to create a CartItem object 
    and add it to the Cart object.
    
    This API endpoint allows authenticated users to add a product to the cart object. 
    It requires the plant ID to be passed in the POST request.
    """
    
    # Restrict access to unauthenticated users
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def post(self, request, *args, **kwargs):
        """Add a cart item to the cart object."""
        
        # Retrieve the Cart object from the database, or return a 404 if it is not found.
        cart = get_object_or_404(Cart, user=request.user)
        
        # Retrieve the Plant object from the database, or return a 404 if it is not found.
        plant = get_object_or_404(Plant, id=request.data.get('plant_id'))
        
        # Create a CartItem object
        # Quantity is equal to 1 by default
        cartItem = CartItem.objects.create(cart=cart, product=plant, quantity=1)
        
        return Response(status=status.HTTP_200_OK)