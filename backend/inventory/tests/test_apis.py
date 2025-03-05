from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from inventory.models import Plant
from inventory.serializers import PlantSerializer
from .base_test import FileUploadTestCase # Custom class for file handling




class PlantListAPITest(FileUploadTestCase):
    """
    Test case for verifying the functionalities of the PlantListAPI view.
    
    
    FileUploadTestCase is a custom base test case class that provides utility methods
    to handle file uploads in Django tests. It automates the setup of a temporary
    directory for storing uploaded files, ensuring that the `MEDIA_ROOT` is configured
    properly during the test. It also ensures that files are cleaned up and deleted
    after each test is run, preventing test pollution and improving isolation.
     
        
    - Verify that the API returns data from the database.
    - Test the behavior when there is no data in the database.
    """
    
    
    def setUp(self):
        
        super().setUp()  # Call the setUp of FileUploadTestCase to handle media root setup
        
        # Initialize the APIClient instance for testing 
        self.client = APIClient() # Create a new instance of the APIClient
        self.url = reverse('plant-list') # Get the URL endpoint
        
        self.image = self.create_valid_image() # Create a valid image for testing purpose
        
        
        # Create a few Plant objects
        Plant.objects.create(name='Rosa', price=12.50, image=self.image)
        Plant.objects.create(name='Violet', price=10.00, image=self.image)
        Plant.objects.create(name='Chamomile', price=52.10, image=self.image)
    
    
    def test_get_plants_success(self):
        """Test that a GET request to the PlantListAPI returns a successful response with plants data."""
        
        # Make a GET request to the plant-list endpoint
        response = self.client.get(self.url)
        
        # Assert the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert that the correct number of plants is returned in the response
        plants = Plant.objects.all() # Get all the Plant objects from the database
        serializer = PlantSerializer(plants, many=True) # Serialize data
        self.assertEqual(response.data, serializer.data) # Check if the response data is equal to the serialized data.
    
    
    def test_get_plants_not_found(self):
        """Test that a GET request to the PlantListAPI returns a 404 response when n plants exist in the db."""
        
        # Delete all the plants in the database
        Plant.objects.all().delete()
        
        # Make a GET request to the plant-list endpoint
        response = self.client.get(self.url)
        
        # Assert the status code is 404 (Not found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
        # Assert that the response message matches the expected error message
        self.assertEqual(response.data['detail'], 'No plants found.')