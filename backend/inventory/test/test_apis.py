import uuid

from rest_framework.test import APIClient
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
        Plant.objects.create(name='Violet', price=10.00, rating=4, image=self.image)
        Plant.objects.create(name='Chamomile', price=52.10, rating=5, image=self.image)
    
    
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
        
        
class PlantDetailAPITest(FileUploadTestCase):
    """
    Test the behavior of the PlantDetailAPITest endpoint.
    
    FileUploadTestCase is a custom base test case class that provides utility methods
    to handle file uploads in Django tests. It automates the setup of a temporary
    directory for storing uploaded files, ensuring that the `MEDIA_ROOT` is configured
    properly during the test. It also ensures that files are cleaned up and deleted
    after each test is run, preventing test pollution and improving isolation.
    
    - Verify that the API returns data from the database
    - Test the behavior when there is no data in the database
    - Verify that the in_stock field is correct.
    - Verify that the discounted price is calculated correctly.
    """
    
    def setUp(self):
        
        super().setUp() # Call the setUp of the FileUploadTestCase to handle media root setup
        
        # Initial the APIClient instance for testing
        self.client = APIClient()
        
        
        # Create a few Plant objects
        self.plant_1 = Plant.objects.create(
            name='Rosa',
            price=15.00,
            image=self.create_valid_image(),
            discount_percentage=10
        )

        self.plant_2 = Plant.objects.create(name='Violet', price=12.50, image=self.create_valid_image())
        
        
    def test_plant_detail_success(self):
        """Test that the PlantDetailAPI returns correct details for an existing plant."""
        
        
        # Make a GET request to the plant detail endpoint with the plant's UUID
        response = self.client.get(reverse('plant-detail', args=[self.plant_2.id]))
        
        # Assert the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the plant data returned matches the expected data
        self.assertEqual(response.data['name'], self.plant_2.name)
        self.assertEqual(response.data['rating'], self.plant_2.rating)
        self.assertAlmostEqual(float(response.data['price']), self.plant_2.price)
        self.assertEqual(response.data['image'], '/media/' + self.plant_2.image.name)
        
        
    def test_plant_detail_not_found(self):
        """Test that the PlantDetailAPI returns a 404 when the plant is not found."""
        
        # Generate a random UUID that does not exist in the database
        non_existent_uuid = uuid.uuid4()
        
        # Make a GET request to the plant detail endpoint with the non-existent UUID
        response = self.client.get(reverse('plant-detail', args=[non_existent_uuid]))
        
        
        # Assert the status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_in_stock_field(self):
        """Make sure that the in_stock field is correct"""

        # Create a plant object with a stock_count greater than 0
        plantObj_1 = Plant.objects.create(
            name='Rosa',
            price=13.50,
            image=self.create_valid_image(),
            stock_count=50 # The in_stock field should be true
        )

        # Make a GET request to the plant detail API endpoint with the plant's UUID
        response = self.client.get(reverse('plant-detail', args=[plantObj_1.id]))
        self.assertTrue(response.data['in_stock'])

        # Create a plant object with a stock_count equal to 0
        plantObj_2 = Plant.objects.create(
            name='Violet',
            price=15.30,
            image=self.create_valid_image(),
            stock_count=0 # The in_stock field should be false
        )

        # Make a GET request to the plant detail API endpoint with the plant's UUID
        response = self.client.get(reverse('plant-detail', args=[plantObj_2.id]))
        self.assertFalse(response.data['in_stock'])


    def test_discounted_price_field(self):
        """Make sure that the discounted_price field is calculated correctly"""

        # Make a GET request to the plant detail API endpoint with the plant's UUID
        response = self.client.get(reverse('plant-detail', args=[self.plant_1.id]))
        self.assertEqual(response.data['discounted_price'], 13.5) # 15.00 - 10% = 13.5