from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404


from .models import Plant
from .serializers import PlantSerializer


class PlantListAPI(APIView):
    """
    Handles GET requests and returns a list of Plant objects. 
    """
    
    permission_classes = [AllowAny] # Allow access for all users
    
    def get(self, request, *args, **kwargs):
        """Retrieve the Plant objects from the database and return them as a JSON response."""
        
        plants = Plant.objects.all() # Retrieve all the objects from the database
        
        
        # Return 404 if no plants are found, otherwise return serialized data
        if not plants:
            return Response({'detail': 'No plants found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the data to convert it into JSON format
        serializer = PlantSerializer(plants, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlantDetailAPI(APIView):
    """
    PlantDetailAPI provides a detailed view of a specific plant identified by its UUID.
    
    This API endpoint allows clients to retrieve a detailed view of a specific plant 
    using its UUID. It supports a GET request where the plant's unique id is 
    passed as a URL parameter. The response returns the plant's attributes in JSON format.
    """
    
    permission_classes = [AllowAny] # Allow access for all users
    
    
    def get(self, request, id, *args, **kwargs):
        """Handles a GET request to fetch plant details by its UUID."""
        
        # Retrieve the object from the database
        plant = get_object_or_404(Plant, id=id)
        
        # Serialize the plant object into a JSON response
        serializer = PlantSerializer(plant)
        
        return Response(serializer.data, status=status.HTTP_200_OK)