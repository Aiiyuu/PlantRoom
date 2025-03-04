import uuid
import os
import shutil

from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from inventory.models import Plant


TEST_DIR = 'test_plant' # A name for a new test directory used to store uploaded test files


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class PlantModelTest(TestCase):
    """
    Test the functionalities of the Plant model to ensure that all methods are working correctly.
    

    - Test plant creation.
    - Test that the UUID is generated automatically.
    - Test that the UUID is unique.
    - Test that the UUID is consistant on save.
    - Test invalid name length.
    - Test that leading and trailing spaces are stripped
    - Test invalid description.
    - Test negatve and longer than 10 digits price.
    - Test negative stock_count.
    - Test invalid discount_percentage field.
    - Test invalid image format.
    - Test image size limits.
    - Test image upload path.
    - Test the get_discounted_price method.
    - Test the in_stock property.
    - Test that the __str__ method correctly represents a Plant object
    """
        
    
    def setUp(self):
        """Create assets for the tests aformentioned."""
        
        # Create a mock image file (in this case, a fake JPEG file)
        self.correct_image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake image content',
            content_type='image/jpeg' # Simulated MIME type for a JPEG image
        )
        
        
        # Create a Plant object with correct data
        self.correct_plant_object = Plant.objects.create(
            name='Aloe Vera',
            description='A succulent plant known for its medicinal properties and soothing gel.',
            price=20.00,
            discount_percentage=10,
            stock_count=120,
            image=self.correct_image_file
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
            image=self.correct_image_file
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
            image=self.correct_image_file
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
            image=self.correct_image_file
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
            image=self.correct_image_file
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
            image=self.correct_image_file
        )
        
        
        plant.clean() # Call the clean method, which should stip all the leading/trailing spaces
        
        self.assertEqual(plant.name, 'Rosa') # Ensure that the spaces have been removed
        
    
    def test_invalid_description(self):
        """Test that the description field is no longer than 1500 characters."""
        
        # Create a new Plant instance with an invalid description
        plant = Plant(
            name='Rosa',
            description='A' * 1501,
            price=22.50,
            image=self.correct_image_file
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
            image=self.correct_image_file
        )
        
        # Check if the new plant instance raises a ValidationError
        with self.assertRaises(ValidationError):
            plant.clean()
            
            
        # Create a new plant instance with an invalid price value
        plant = Plant(
            name='Rosa',
            price=10000000000.50, # It must be 10 digits before the decimal point
            image=self.correct_image_file
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
            image=self.correct_image_file
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
            image=self.correct_image_file
        )
        
        # Check if the new Plant instance triggers a ValidationError after calling the clean method
        with self.assertRaises(ValidationError):
            plant.clean()
            
            
    def test_invalid_image_format(self):
        """Test that a Plant object with an incorrect image format, cannot be saved to the database."""
        
        # Create a mock image file (in this case with the unsupported format, gif)
        incorrect_image_file = SimpleUploadedFile(
            name='invalid_format.gif',
            content=b'fake image content',
            content_type='image/gif' # Simulated MIME type for a GIF image
            # Only PNG, JPG or JPEG formats are allowed
        )
        
        
        # Create a new Plant object with the invalid image field
        plant = Plant(
            name='Rosa',
            price=15.00,
            image=incorrect_image_file
        )
        
        
        # Check if the clean method raises a validation error for the created plant object
        with self.assertRaises(ValidationError):
            plant.clean()
            
        
    def test_image_size_limit(self):
        """Ensure that a Plant object cannot be saved if the image field size exceeds allowed 10MB"""
        
        # Create a mock image file (in this case with a data parameter that exceeds the allowed 10MB)
        large_file_size = SimpleUploadedFile(
            name='large_image.jpeg',
            content=b'Fake image content',
            content_type='image/jpeg'
        )
        
        large_file_size.size = (10 * 1024 * 1024) + 1
        
        # Create a new Plant object with an incorrect image field
        plant = Plant(
            name='Rosa',
            price=10.00,
            image=large_file_size # Only 10MB is allowed
        )
        
        # Check that the clean method raises a ValidationError for the image field
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
        plant_1 = Plant(name='Rosa', price=10.00, stock_count=50, image=self.correct_image_file)
        
        # Create a new Plant object to test if the in-stock property will
        # return False when the stock_count is equal to zero
        plant_2 = Plant(name='Rosa', price=10.00, stock_count=0, image=self.correct_image_file)
        
        self.assertTrue(plant_1.in_stock) # Should return True
        self.assertFalse(plant_2.in_stock) # Should return False
        
    
    def test_str_method(self):
        """Ensure that the __str__ method represents a Plant object in a human-readable way."""
        
        # Ensure that the __str__ method returns the name of the Plant object
        self.assertEqual(str(self.correct_plant_object), self.correct_plant_object.name)
        
    
    def tearDown(self):
        """Remove the test directory used to store the uploaded fiels for the tests."""
        
        # Check if the directory exists to remove it
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)

                
                
        super().tearDown()  # Ensure any other tearDown logic is also called