from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from cart.models import Cart, CartItem
from account.models import User
from inventory.models import Plant
from inventory.test.base_test import FileUploadTestCase

import uuid



class CartModelTest(FileUploadTestCase):
    """
    Test the functionalitites of the Cart model.
    
    FileUploadTestCase is a custom base test case class that provides utility methods
    to handle file uploads in Django tests. It automates the setup of a temporary
    directory for storing uploaded files, ensuring that the `MEDIA_ROOT` is configured
    properly during the test. It also ensures that files are cleaned up and deleted
    after each test is run, preventing test pollution and improving isolation.
    
    Tests:
        - Test the Cart creation.
        - Test that the UUID is generated automatically.
        - Test that the UUID is unique.
        - Test that the UUID is consistant on save.
        - Test the related_name for the user field.
        - Test that the get_total method is working correctly.
        - Test that the get_items_count is working correctly.
        - Test that the __str__ method represents objects correctly.
        - Test the cart deletion on user deletion.
        - Test that the user has only one cart.
    """
    
    def setUp(self):
        
        super().setUp()  # Make sure to call the parent setUp to initialize file handling
        
        # Create two regular user objects
        self.test_user1 = User.objects.create_user(name='test_user1', email='test_1@test.com', password='a12a14t56')
        self.test_user2 = User.objects.create_user(name='test_user2', email='test_2@test.com', password='a12a14t56')
        
        
        # Create two Cart objects
        self.test_cart1 = Cart.objects.create(user=self.test_user1) # Refers to the test_user1
        self.test_cart2 = Cart.objects.create(user=self.test_user2) # Refers to the test_user2
        
        
        # Create a few Plant objects
        self.test_plant1 = Plant.objects.create(name='Rosa', price=10.50, image=self.create_valid_image())
        self.test_plant2 = Plant.objects.create(name='Violet', price=16.99, image=self.create_valid_image())
        
        
        # Create a few CartItmes object
        self.test_cart_item1 = CartItem.objects.create(cart=self.test_cart1, product=self.test_plant1, quantity=3)
        self.test_cart_item2 = CartItem.objects.create(cart=self.test_cart1, product=self.test_plant2)
        
        
    def test_cart_creation(self):
        """Ensure that a Cart object is created successfully with correct data."""
        
        # Create a regular User object for the test
        user = User.objects.create_user(name='test', email='test@test.com', password='test123')
        
        # Create a cart object 
        cart = Cart.objects.create(user=user)
        
        # Assert the correct user is saved in the cart's user field.
        self.assertEqual(cart.user, user)
        
        
        
    def test_cart_uuid_is_generated_automatically(self):
        """Ensure that the UUID field is generated automatically."""
        
        self.assertIsInstance(self.test_cart1.id, uuid.UUID) # Ensure that the cart.id is UUID
        self.assertIsNotNone(self.test_cart1.id) # Ensure that the UUID field is not None
        
    
    def test_uniqueness_of_uuid(self):
        """Test that the new Cart object has a different UUID from the one created in the setup function."""
        
        # Create a regular User object for the test
        user = User.objects.create_user(name='test', email='test@test.com', password='test123')
        
        # Create a new Cart object
        cart = Cart.objects.create(user=user)
        
        self.assertNotEqual(cart.id, self.test_cart1.id) # Ensure that the uuid field is not the same
        
        
    def test_uuid_consistancy_on_save(self):
        """Test that the UUID does not change after saving the object again."""
        
        # Assign the Cart object created in the setUp method to the 'cart' variable
        cart = self.test_cart1
        
        initial_uuid = cart.id # Asssign the old uuid before saving 
        
        cart.save() # Save the cart object again
        
        self.assertEqual(cart.id, initial_uuid) # Assert the UUIDs are equal
        
        
    def test_user_field_related_name(self):
        """Test the behavior of the related_name in the user field."""
        
        # Test that you can get cart by the user model instance
        self.assertIsNotNone(self.test_user1.cart)
        
    
    def test_get_total(self):
        """Ensure that the get_total method is working correctly."""
        
        # Ensure that the get_total method calculates the data correctly.
        self.assertEqual(float(self.test_cart1.get_total()), 48.49)
        
        
    def test_get_items_count(self):
        """Ensure that the get_items_count method is working correctly."""
        
        # Test that the number of items in the cart is 4.
        self.assertEqual(self.test_cart1.get_items_count(), 4)
        
    
    def test_str_method(self):
        """Ensure that the __str__ method represents a Cart object in a human-readable way."""
        
        # Ensure that the __str__ method returns a user's email
        self.assertEqual(str(self.test_cart1), self.test_user1.email)
        
    
    def test_cart_deletion_on_user_deletion(self):
        """Test that the Cart object is deleted when the user object is deleted."""
        
        user = self.test_user2 # Declare the user variable with the user instance.
        cart_id = self.test_cart2.id # Get the cart ID before deleting the user
        
        # First, assert that the cart exists before deletion
        self.assertEqual(Cart.objects.filter(user=user).count(), 1)
        
        user.delete() # Now, delete the user
        
        # Assert that the cart related to the user is also deleted        
        self.assertEqual(Cart.objects.filter(id=cart_id).count(), 0)
   
    
    def test_user_has_only_one_cart(self):
        """Ensure that a user can only have one cart."""
        
        # Trying to create a new Cart object related to a user who already has one
        # An IntegrityError error should occur
        with self.assertRaises(IntegrityError):
            Cart.objects.create(user=self.test_user1)
            
       
            
class CartItemTest(FileUploadTestCase):
    """
    Test the functionalitites of the CartItem model.
    
    FileUploadTestCase is a custom base test case class that provides utility methods
    to handle file uploads in Django tests. It automates the setup of a temporary
    directory for storing uploaded files, ensuring that the `MEDIA_ROOT` is configured
    properly during the test. It also ensures that files are cleaned up and deleted
    after each test is run, preventing test pollution and improving isolation.
    
    Tests:
        - Test the Cart creation.
        - Test that the UUID is generated automatically.
        - Test that the UUID is unique.
        - Test that the UUID is consistant on save.
        - Test the related_name for the cart field.
        - Test that the get_total_price method is working correctly
        - Test that the __str__ method represents objectes correctly.
        - Test the CartItem object deletion on the Plant or Cart objects deletion.
    """
    
    
    def setUp(self):
        super().setUp() # Make sure to call the parent setUp to initialize file handling
    
        # Create two regular user objects
        self.test_user1 = User.objects.create_user(name='test_user1', email='test_1@test.com', password='a12a14t56')
        self.test_user2 = User.objects.create_user(name='test_user2', email='test_2@test.com', password='a12a14t56')
        
        
        # Create two Cart objects
        self.test_cart1 = Cart.objects.create(user=self.test_user1) # Refers to the test_user1
        self.test_cart2 = Cart.objects.create(user=self.test_user2) # Refers to the test_user2
        
        
        # Create a few Plant objects
        self.test_plant1 = Plant.objects.create(name='Rosa', price=10.50, image=self.create_valid_image())
        self.test_plant2 = Plant.objects.create(name='Violet', price=16.99, image=self.create_valid_image())
        
        
        # Create a few CartItmes object
        self.test_cart_item1 = CartItem.objects.create(cart=self.test_cart1, product=self.test_plant1, quantity=3)
        self.test_cart_item2 = CartItem.objects.create(cart=self.test_cart1, product=self.test_plant2)
        
        
    def test_cart_item_creation(self):
        """Ensure that the CartItem object is created and correctly saved to the database."""
        
        # Create a regular User object for the test
        user = User.objects.create_user(name='test', email='test@test.com', password='test123')
        
        # Create a cart object for the test
        cart = Cart.objects.create(user=user)
        
        # Create a plant object for the test
        plant = Plant.objects.create(name='Chamomile', price=10.20, image=self.create_valid_image())

        # Create a cart item object
        cartItem = CartItem.objects.create(cart=cart, product=plant)
        
        # Assert that the correct cart object is saved in the cart item's user field.
        self.assertEqual(cartItem.cart, cart)
        # Assert that the correct plant object is saved in the cart item's product field.
        self.assertEqual(cartItem.product, plant)
        # Assert the quantity field is equal to one by default
        self.assertEqual(cartItem.quantity, 1)
        
        
        # Get the current time to check against
        now = timezone.now()
        
        # Check that the added_at is close to the current time
        # Allow a small margin for creation time
        time_diff = now - cartItem.added_at
        
        # Assert that the correct date and time are saved in the cart item's added_at field.
        self.assertLess(time_diff.total_seconds(), 5) # The margin could be up to 5 seconds
        
        
    def test_cart_item_uuid_is_generated_automatically(self):
        """Ensure that the UUID field is generated automatically."""
        
        self.assertIsInstance(self.test_cart_item1.id, uuid.UUID) # Ensure that the cart.id is UUID
        self.assertIsNotNone(self.test_cart_item1.id) # Ensure that the UUID field is not None
        
    
    def test_uniqueness_of_uuid(self):
        """Test that the new CartItem object has a different UUID from the one created in the setup function."""
        
        # Create a regular User object for the test
        user = User.objects.create_user(name='test', email='test@test.com', password='test123')
        
        # Create a cart object for the test
        cart = Cart.objects.create(user=user)
        
        # Create a plant object for the test
        plant = Plant.objects.create(name='Chamomile', price=10.20, image=self.create_valid_image())
        
        # Create a new Cart Item object
        cart_item = CartItem.objects.create(cart=cart, product=plant)
        
        self.assertNotEqual(cart_item.id, self.test_cart_item1.id) # Ensure that the uuid field is not the same
        
        
    def test_uuid_consistancy_on_save(self):
        """Test that the UUID does not change after saving the object again."""
        
        # Assign the Cart object created in the setUp method to the 'cart' variable
        cart_item = self.test_cart_item1
        
        # Temporarily bypass the clean method to avoid validation error
        cart_item.clean = lambda: None  # Mock clean method to do nothing
        
        initial_uuid = cart_item.id # Asssign the old uuid before saving 
        
        cart_item.save() # Save the cart object again
        
        self.assertEqual(cart_item.id, initial_uuid) # Assert the UUIDs are equal
        
        
    def test_cart_field_related_name(self):
        """Test the behavior of the related_name in the user field."""
        
        # Test that you can get cart by the user model instance
        self.assertTrue(self.test_cart1.cart_items)
    
    
    def test_get_total_price(self):
        """Ensure that the get_total_price method is working correctly."""
    
        self.assertEqual(self.test_cart_item1.get_total_price(), 31.5)
        
        
    def test_str_method(self):
        """Ensure that the __str__ method represents a CartItem object in a human-readable way."""
        
        # Ensure that the __str__ method returns a product's name.
        self.assertEqual(str(self.test_cart_item1), self.test_plant1.name) 


    def test_cart_item_deletion_on_cart_deletion(self):
        """Test that the CartItem object is deleted when the cart object is deleted."""
        
        cart = self.test_cart1 # Declare a cart variable with a self.test_cart1 instance.
        plant = self.test_plant1 # Declare a plant variable with a self.test_plant1 instance.
        cart_item_id = self.test_cart_item1.id # Get the cart_item ID before deleting the cart object
        
        
        # First, assert that the cart_item exists before deletion
        self.assertEqual(CartItem.objects.filter(cart=cart, product=plant).count(), 1)
        
        cart.delete() # Now, delete the cart object
        
        # Assert that the cart related to the user is also deleted        
        self.assertEqual(Cart.objects.filter(id=cart_item_id).count(), 0)
        
        
    def test_cart_item_deletion_on_product_deletion(self):
        """Test that the CartItem object is deleted when the plant object is deleted."""
        
        cart = self.test_cart1 # Declare a cart variable with a self.test_cart1 instance.
        plant = self.test_plant1 # Declare a plant variable with a self.test_plant1 instance.
        cart_item_id = self.test_cart_item1.id # Get the cart_item ID before deleting the cart object
        
        
        # First, assert that the cart_item exists before deletion
        self.assertEqual(CartItem.objects.filter(cart=cart, product=plant).count(), 1)
        
        plant.delete() # Now, delete the cart object
        
        # Assert that the cart related to the user is also deleted        
        self.assertEqual(Cart.objects.filter(id=cart_item_id).count(), 0)
