import uuid

from django.test import TestCase
from django.core.exceptions import ValidationError
from inventory.models import Plant
from .base_test import FileUploadTestCase # Custom class for file handling


class PlantModelTest(FileUploadTestCase):
    """
    Test the functionalities of the Plant model to ensure that all methods are working correctly.
    
    FileUploadTestCase is a custom base test case class that provides utility methods
    to handle file uploads in Django tests. It automates the setup of a temporary
    directory for storing uploaded files, ensuring that the `MEDIA_ROOT` is configured
    properly during the test. It also ensures that files are cleaned up and deleted
    after each test is run, preventing test pollution and improving isolation.
    

    - Test plant creation.
    - Test that the UUID is generated automatically.
    - Test that the UUID is unique.
    - Test that the UUID is consistent on save.
    - Test invalid name length.
    - Test that leading and trailing spaces are stripped
    - Test invalid description.
    - Test negative and longer than 10 digits price.
    - Test negative stock_count.
    - Test invalid discount_percentage field.
    - Test invalid image format.
    - Test image size limits.
    - Test invalid rating handling
    - Test image upload path.
    - Test the get_discounted_price method.
    - Test the in_stock property.
    - Test that the __str__ method correctly represents a Plant object
    """
        
    
    def setUp(self):
        """Create assets for the tests aformentioned."""
        
        super().setUp()  # Make sure to call the parent setUp to initialize file handling
        
        # Create a Plant object with correct data
        self.correct_plant_object = Plant.objects.create(
            name='Aloe Vera',
            description='A succulent plant known for its medicinal properties and soothing gel.',
            price=20.00,
            discount_percentage=10,
            stock_count=120,
            image=self.create_valid_image()
        )
    
    
    def test_plant_creation(self):
        """Ensure that a Plant object is created successfully with correct data."""
        
        # Create a Plant object with correct data
        plant = Plant.objects.create(
            name='Rosa',
            description='A beautiful flower.',
            price=10.00,
            discount_percentage=20,
            stock_count=50,
            image=self.create_valid_image()
        )
        
        
        # Ensure that the name is equal to what was save to the DB
        self.assertEqual(plant.name, 'Rosa')
        
        # Ensure that the description is equal to what was save to the DB
        self.assertEqual(plant.description, 'A beautiful flower.')
        
        # Ensure that the price is equal to what was save to the DB
        self.assertEqual(plant.price, 10.00)
        
        # Ensure that the discount_percentage is equal to what was save to the DB
        self.assertEqual(plant.discount_percentage, 20)
        
        # Ensure that the stock_count is equal to what was save to the DB
        self.assertEqual(plant.stock_count, 50)
        
    
    def test_uuid_is_generated_automatically(self):
        """Test that the UUID is automatically generated when a new Plant object is created."""
        
        self.assertIsInstance(self.correct_plant_object.id, uuid.UUID) # Check if the id is of type UUID
        self.assertIsNotNone(self.correct_plant_object.id) # Ensure the UUID is not None
        
        
    def test_uuids_are_unique(self):
        """Test that a new Plant object cannot be created if the UUID is already taken."""
        
        # Create a new Plant object
        new_plant_object = Plant.objects.create(
            name='Fiddle Leaf Fig',
            price=85.50,
            image=self.create_valid_image()
        )
        
        # Ensure that the UUIDs of two plant objects are not the same
        self.assertNotEqual(self.correct_plant_object.id, new_plant_object.id)
        
        
    def test_uuid_consistency_on_save(self):
        """Test that the UUID does not change after saving the object."""
        
        # Get the created Plant object
        plant = self.correct_plant_object
        
        initial_uuid = plant.id # Get the UUID before saving it again
        
        plant.save() # Save the Plant object again
        self.assertEqual(initial_uuid, plant.id) # UUID should not change
        

    def test_invalid_name(self):
        """
        Test that the Plant object cannot be created if the length is not between 3 and 100 
        characters or is not provided.
        """
        
        # Create A Plant object instance with invalid name length
        plant = Plant(
            name='lv',
            price=22.50,
            image=self.create_valid_image()
        )
        
        # Test that it raises a ValidationError when the clean method is called.
        with self.assertRaises(ValidationError):
            plant.clean()
            
            
        # Create A Plant object instance with no name field provided
        plant = Plant(
            description='A fragrant herb widely used for relaxation and stress relief.',
            price=22.50,
            discount_percentage=15,
            stock_count=80,
            image=self.create_valid_image()
        )
        
        # Test that it raises a ValidationError when the clean method is called.
        with self.assertRaises(ValidationError):
            plant.clean()
            
            
    def test_name_stripping_spaces(self):
        """Test that the leading and trailing spaces are stripped."""
        
        # Create a new Plant object instance
        plant = Plant(
            name='     Rosa   ',
            price=22.50,
            image=self.create_valid_image()
        )
        
        
        plant.clean() # Call the clean method, which should strip all the leading/trailing spaces
        
        self.assertEqual(plant.name, 'Rosa') # Ensure that the spaces have been removed
        
    
    def test_invalid_description(self):
        """Test that the description field is no longer than 1500 characters."""
        
        # Create a new Plant instance with an invalid description
        plant = Plant(
            name='Rosa',
            description='A' * 1501,
            price=22.50,
            image=self.create_valid_image()
        )
        
        # Check if the clean method raises a ValidationError
        with self.assertRaises(ValidationError):
            plant.clean()
            
            
    def test_invalid_price(self):
        """Test that the price field cannot be negative and no longer than 10 digits."""
        
        # Create a new plant instance with an invalid price value
        plant = Plant(
            name='Rosa',
            price=-10.50, # It must be a positive value
            image=self.create_valid_image()
        )
        
        # Check if the new plant instance raises a ValidationError
        with self.assertRaises(ValidationError):
            plant.clean()
            
            
        # Create a new plant instance with an invalid price value
        plant = Plant(
            name='Rosa',
            price=10000000000.50, # It must be 10 digits before the decimal point
            image=self.create_valid_image()
        )
        
        # Check if the new plant instance raises a ValidationError after calling the clean method
        with self.assertRaises(ValidationError):
            plant.clean()
            
            
    def test_invalid_stock_count(self):
        """Test that the stock_count field cannot be negative."""
        
        # Create a new Plant instance with an invalid stock_count field 
        plant = Plant(
            name='Rosa',
            price=10.50,
            stock_count=-10, # It must be a positive value
            image=self.create_valid_image()
        )
        
        # Check if the new Plant instance raises a ValidationError after calling the clean method
        with self.assertRaises(ValidationError):
            plant.clean()
            
            
    def test_invalid_discount_percentage(self):
        """Test that the discount_percentage field is between 0 and 100, inclusive."""
        
        # Create a new Plant instance with an invalid discount_percentage field 
        plant = Plant(
            name='Rosa',
            price=10.50,
            discount_percentage=110, # It must be between 0 and 100 (inclusively)
            image=self.create_valid_image()
        )
        
        # Check if the new Plant instance triggers a ValidationError after calling the clean method
        with self.assertRaises(ValidationError):
            plant.clean()
            
            
    def test_invalid_image_format(self):
        """Test that a Plant object with an incorrect image format, cannot be saved to the database."""
        
        
        # Create a new Plant object with the invalid image field
        plant = Plant(
            name='Rosa',
            price=15.00,
            image=self.create_invalid_image() # Returns a GIF image
        )
        
        
        # Check if the clean method raises a validation error for the created plant object
        with self.assertRaises(ValidationError):
            plant.clean()
            
        
    def test_image_size_limit(self):
        """Ensure that a Plant object cannot be saved if the image field size exceeds allowed 10MB"""
        
        
        # Create a new Plant object with an incorrect image field
        plant = Plant(
            name='Rosa',
            price=10.00,
            image=self.create_large_image() # Returns a 15MB image
        )
        
        # Check that the clean method raises a ValidationError for the image field
        with self.assertRaises(ValidationError):
            plant.clean()


    def test_invalid_rating_handling(self):
        """Ensure that a Plant object cannot be saved if the rating is negative or greater than 5"""

        # Create a new Plant object that has an incorrect rating
        plant = Plant(
            name='Verdant Nest',
            price=14.30,
            image=self.create_valid_image(),
            rating=-4 # Specify an invalid rating
        )

        # Check that the clean method raises a ValidationError for the rating field
        with self.assertRaises(ValidationError):
            plant.clean()

        # Create a new Plant object that has an incorrect rating
        plant = Plant(
            name='Verdant Nest',
            price=14.30,
            image=self.create_valid_image(),
            rating=-4 # Specify an invalid rating
        )

        # Check that the clean method raises a ValidationError for the rating field
        with self.assertRaises(ValidationError):
            plant.clean()
        
    
    def test_image_upload_path(self):
        """Test that images from the plant model are saved in the correct directory."""
        
        # Check the media path where the image was saved
        expected_image_path = f'plants/{self.correct_plant_object.id}.jpg'
        
        # Ensure it starts with the correct folder
        self.assertTrue(self.correct_plant_object.image.name.startswith('plants/'))
        
      
    def test_get_discount_price_method(self):
        """Test that the get_discount_method calculates and returns the correct value."""
        
        # Recieve a value from the the get_discounted_price
        output = self.correct_plant_object.get_discounted_price()
        
    
    def test_in_stock_property(self):
        """Test that the in-stock property returns the expected boolean value."""
        
        # Create a new Plant object to test if the in-stock property will 
        # return True when the stock_count is greater than zero.
        plant_1 = Plant(name='Rosa', price=10.00, stock_count=50, image=self.create_valid_image())
        
        # Create a new Plant object to test if the in-stock property will
        # return False when the stock_count is equal to zero
        plant_2 = Plant(name='Rosa', price=10.00, stock_count=0, image=self.create_valid_image())
        
        self.assertTrue(plant_1.in_stock) # Should return True
        self.assertFalse(plant_2.in_stock) # Should return False
        
    
    def test_str_method(self):
        """Ensure that the __str__ method represents a Plant object in a human-readable way."""
        
        # Ensure that the __str__ method returns the name of the Plant object
        self.assertEqual(str(self.correct_plant_object), self.correct_plant_object.name)