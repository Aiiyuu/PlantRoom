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
    
    # Restrict access for unauthenticated users
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def post(self, request, *args, **kwargs):
        """Add a cart item to the cart object."""
        
        # Retrieve the Cart object from the database or return a 404 if it is not found.
        cart = get_object_or_404(Cart, user=request.user)
        
        # Retrieve the Plant object from the database or return a 404 if it is not found.
        plant = get_object_or_404(Plant, id=request.data.get('plant_id'))
        
        # Create a CartItem object
        # Quantity is equal to 1 by default
        cartItem = CartItem.objects.create(cart=cart, product=plant, quantity=1)
        
        return Response(status=status.HTTP_200_OK)


class DeleteCartItemAPI(APIView):

     """
        The DeleteCartItemAPI handles a DELETE request to remove a specific CartItem object
        from the database, based on the product_id parameter passed by the user.

        This API endpoint allows authenticated users to delete a product they have added
        to the cart. It requires them to pass the product ID.
     """

     # Restriction access for unauthenticated users
     authentication_classes = [SessionAuthentication]
     permission_classes = [IsAuthenticated]

     def delete(self, request, id, *args, **kwargs):
         """Delete a CartItem from the user's cart"""

         # Retrieve the Cart object from the database or return 404 if it is not found
         cart = get_object_or_404(Cart, user=request.user)

         # Retrieve the Plant object from the database or return 404 if it's not found
         plant = get_object_or_404(Plant, id=id)

         # Retrieve the CartItem object
         cart_item = get_object_or_404(CartItem, cart=cart, product=plant)

         cart_item.delete() # Delete the CartItem from the database

         return Response(status=status.HTTP_204_NO_CONTENT)


class IncreaseQuantityAPI(APIView):
    """
    The IncreaseQuantityAPI handles a PATCH request that increases
    the quantity of a CartItem object by 1.

    This API endpoint allows authenticated users to increase the quantity
    of an object by one. It requires them to provide the product ID.
    """

    # Restriction access for unauthenticated users
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, id, *args, **kwargs):
        """Increase the quantity of the CartItem object by one."""

        # Retrieve the Cart object from the database or return 404 if it is not found
        cart = get_object_or_404(Cart, user=request.user)

        # Retrieve the Plant object from the database or return 404 if it's not found
        plant = get_object_or_404(Plant, id=id)

        # Retrieve the CartItem object
        cart_item = get_object_or_404(CartItem, cart=cart, product=plant)

        cart_item.quantity += 1 # Increase the amount
        cart_item.save() # Save to the database

        return Response(status=status.HTTP_200_OK)



class DecreaseQuantityAPI(APIView):
    """
    The DecreaseQuantityAPI handles a PATCH request that decreases
    the quantity of a CartItem object by 1.

    This API endpoint allows authenticated users to decrease the quantity
    of an object by one. It requires them to provide the product ID. If the
    quantity is equal to 1, the CartItem will be deleted.
    """

    # Restriction access for unauthenticated users
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, id, *args, **kwargs):
        """Decrease the quantity of the CartItem object by one."""

        # Retrieve the Cart object from the database or return 404 if it is not found
        cart = get_object_or_404(Cart, user=request.user)

        # Retrieve the Plant object from the database or return 404 if it's not found
        plant = get_object_or_404(Plant, id=id)

        # Retrieve the CartItem object
        cart_item = get_object_or_404(CartItem, cart=cart, product=plant)

        # Check if the quantity is equal to 1
        if cart_item.quantity == 1:
            # Delete the CartItem if the if statement returns True.
            cart_item.delete() # Delete the object
            return Response(status=status.HTTP_204_NO_CONTENT)

        cart_item.quantity -= 1 # Decrease the amount
        cart_item.save() # Save to the database

        return Response(status=status.HTTP_200_OK)