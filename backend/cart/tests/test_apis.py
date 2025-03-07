from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from inventory.tests.base_test import FileUploadTestCase

from account.models import User
from inventory.models import Plant
from cart.models import Cart, CartItem


class CartItemsListAPITest(FileUploadTestCase):
    """
    Test the functionality of the CartItemsListAPI endpoint.
    
    FileUploadTestCase is a custom base test case class that provides utility methods
    to handle file uploads in Django tests. It automates the setup of a temporary
    directory for storing uploaded files, ensuring that the `MEDIA_ROOT` is configured
    properly during the test. It also ensures that files are cleaned up and deleted
    after each test is run, preventing test pollution and improving isolation.
    
    Tests:
        - Test access for authenticated users.
        - Test access restrictions for unauthenticated users.
        - Test the behavior when the cart is empty.
        - Test the behavior when the Cart object does not exist.
        - Test that the API endpoint successfully returns data.
    """
    
    
    def setUp(self):
        
        super().setUp()  # Call the setUp of FileUploadTestCase to handle media root setup
        
        # Initialize the APIClient instance for testing 
        self.client = APIClient() # Create a new instance of the APIClient
        self.url = reverse('cart-items-list') # Get the URL endpoint
        
        
        # Create a Regular User object
        self.user = User.objects.create_user(name='test_name', email='test@test.com', password='a12a14t56')
        
        # Create a few Plant objects
        self.plant_obj1 = Plant.objects.create(name='Rosa', price=15.00, stock_count=28, image=self.create_valid_image())
        self.plant_obj2 = Plant.objects.create(name='Violet', price=12.90, stock_count=50, image=self.create_valid_image())
        self.plant_obj3 = Plant.objects.create(name='Chamomile', price=3.50, discount_percentage=20, image=self.create_valid_image())
        
        # Create a Cart object
        self.cart = Cart.objects.create(user=self.user)
        
        # Create a few CartItems objects
        self.cart_item_obj1 = CartItem.objects.create(cart=self.cart, product=self.plant_obj1)
        self.cart_item_obj2 = CartItem.objects.create(cart=self.cart, product=self.plant_obj2)
        self.cart_item_obj3 = CartItem.objects.create(cart=self.cart, product=self.plant_obj3)
        
    
    def test_access_for_authenticated_user(self):
        """Test whether an authenticated user can access the cart list API."""
        
        # Login user 
        self.client.force_authenticate(user=self.user)
        
        # Send a GET request to the API endpoint
        response = self.client.get(self.url)
        
        # Assert the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_access_restriction_for_unauthenticated_user(self):
        """Test that unauthenticated users are denied access to the API endpoint."""
        
        # Send a GET request to the API endpoint
        response = self.client.get(self.url)
        
        # Assert the status code is 403 (Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_cart_is_empty(self):
        """Test that the API endpoint returns a 200 status code when the cart items are not found."""
        
        # Make sure the cart is empty before the test
        self.cart.cart_items.all().delete()  # Delete any CartItems if they exist

        # Login user 
        self.client.force_authenticate(user=self.user)

        # Send a GET request to the API endpoint
        response = self.client.get(self.url)

        # Assert that the response status is 200 (OK) for empty cart
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the returned message is correct.
        self.assertEqual(response.data['message'], 'Your cart is empty.')
        
    
    def test_cart_object_not_found(self):
        """
        Ensure that the API endpoint returns a 404 status code when the Cart 
        object does not exist.
        """
        
        # Make sure that the Cart object is deleted before the test
        self.cart.delete()
        
        # Login user
        self.client.force_authenticate(user=self.user)
        
        # Send a GET request to the API endpoint.
        response = self.client.get(self.url)
        
        # Assert the response status is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    
    def test_cart_endpoint_returns_correct_data(self):
        """Test that the API endpoint returns correct data."""
        
        # Login user
        self.client.force_authenticate(user=self.user)
        
        # Send a GET request to the API endpoint
        response = self.client.get(self.url)
        
        # Assert the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Extract the response data
        data = response.json()
        
        # Assert the structure of the response data
        self.assertIn('items', data)
        self.assertIn('total_cart_price', data)
        self.assertIn('total_items_count', data)
        
        # Validate that 'items' contains the expected serialized data
        self.assertEqual(data['total_cart_price'], float(self.cart.get_total())) # Test the total_cart_price method
        self.assertEqual(data['total_items_count'], self.cart.get_items_count()) # Test the total_items_count method
        
        # Assert that the number of items matches the number of created objects.
        self.assertEqual(len(data['items']), len(self.cart.cart_items.all()))
        
        # Ensure that the items include the plant field
        self.assertIn('id', data['items'][0]['product'])
        self.assertIn('name', data['items'][0]['product'])
        self.assertIn('description', data['items'][0]['product'])
        self.assertIn('price', data['items'][0]['product'])
        self.assertIn('stock_count', data['items'][0]['product'])
        self.assertIn('image', data['items'][0]['product'])
        
        
    
class AddCartItemAPITest(FileUploadTestCase):
    """
    Test case for verifying the functionalities of the API endpoint.
    
    FileUploadTestCase is a custom base test case class that provides utility methods
    to handle file uploads in Django tests. It automates the setup of a temporary
    directory for storing uploaded files, ensuring that the `MEDIA_ROOT` is configured
    properly during the test. It also ensures that files are cleaned up and deleted
    after each test is run, preventing test pollution and improving isolation.

    Tests:
        - Test access restriction for unauthenticated users.
        - Test the behavior if the Cart object does not exist.
        - Test the behavior it the Plant object does not exist.
        - Test the behavior when the plant is already added to the cart.
        - Test successful creation of the cart item.
    """
    
    def setUp(self):
        
        super().setUp() # Call the setUp of FileUploadTestCase to handle media root setup
        
        # Initialize the APIClient instance for testing
        self.client = APIClient() # Create a new instance of the APIClient
        self.url = reverse('add-cart-item') # Get the URL endpoint
        
        # Create a regular User object
        self.user = User.objects.create_user(name='test', email='test@test.com', password='a12a14t56')
        
        # Create a Cart object associated with the created User object.
        self.cart = Cart.objects.create(user=self.user)
        
        # Create a Plant object
        self.plant = Plant.objects.create(name='Rose', price=12.50, image=self.create_valid_image())
        
        # Create a CartItem object associated with the created Plant and Cart object.
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.plant)
        

    def test_access_restriction_for_unauthenticated_user(self):
        """Ensure that unauthenticated users cannot create a CartItem object."""
        
        # Make a POST request to the add-cart-item API endpoint
        response = self.client.post(self.url, {'plant_id': str(self.plant.id)})
        
        # Assert the status_code is 403 (Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_cart_object_not_found(self):
        """
        Ensure that the API endpoint correctly handles the case
        when a Cart object is not found.
        """

        # Login user to avoid restrictions
        self.client.force_authenticate(user=self.user)

        # Make sure that the Cart object does not exist before
        # making a POST request to the endpoint.
        self.cart.delete() # Delete the object from the database

        # Make a POST request to the add-cart-item API endpoint.
        response = self.client.post(self.url, {'plant_id': str(self.plant.id)})

        # Assert the status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_plant_object_not_found(self):
        """
        Ensure that the API endpoint correctly handles the case
        when a Plant object is not found.
        """

        # Login user to avoid restrictions
        self.client.force_authenticate(user=self.user)

        # Get the Plant object id before deleting the object.
        plant_id = self.plant.id

        # Make sure that the Plant object does not exist before
        # making a POST request to the endpoint.
        self.plant.delete()

        # Make a POST request to the add-cart-item API endpoint.
        response = self.client.post(self.url, {'product_id': str(plant_id)})

        # Assert the status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_plant_already_added_to_cart(self):
        """
        Ensure that the API endpoint correctly handles the case
        when the Plant object is already added to the cart.
        """

        # Login user to avoid restriction
        self.client.force_authenticate(user=self.user)

        # Trying to create a CartItem that already exists
        # Make a POST request to the add-cart-item API endpoint
        response = self.client.post(self.url, {'product_id': str(self.plant.id)})

        # Ensure that the CartItem object hasn't been created again.
        self.assertEqual(self.cart.cart_items.all().count(), 1)


    def test_successful_creation_of_cart_item(self):
        """Test successful creation of a CartItem object."""

        # Login user to avoid restrictions
        self.client.force_authenticate(user=self.user)

        # Create a new Plant object
        new_plant = Plant.objects.create(name='violet', price=17.15, image=self.create_valid_image())

        # Create a new CartItem object
        new_cart_item = CartItem.objects.create(cart=self.cart, product=new_plant)

        # Check that the CartItem object was created and associated with the Plant
        self.assertIsInstance(new_cart_item, CartItem)
        self.assertEqual(new_cart_item.product, new_plant)  # Ensure the CartItem is linked to the right plant



class DeleteCartItemAPITest(FileUploadTestCase):
    """
    Test case for verifying the functionalities of the DeleteCartItemAPITest endpoint.

    FileUploadTestCase is a custom base test case class that provides utility methods
    to handle file uploads in Django tests. It automates the setup of a temporary
    directory for storing uploaded files, ensuring that the `MEDIA_ROOT` is configured
    properly during the test. It also ensures that files are cleaned up and deleted
    after each test is run, preventing test pollution and improving isolation.

    Tests:
        - Test the endpoint restriction for unauthenticated users.
        - Test the behavior when the Cart object does not exist in the database.
        - Test the behavior when the Plant object does not exist in the database.
        - Test the behavior when the CartItem object does not exist in the database.
        - Test the successful deletion of the CartItem object.
    """

    def setUp(self):

        super().setUp() # Call the setUp of FileUploadTestCase to handle the media root setup

        # Initial the APIClient instance for testing
        self.client = APIClient() # Create a new instance of the APIClient

        # Create a regular User object
        self.user = User.objects.create_user(name='test', email='test@test.com', password='a12a14t56')

        # Create a Cart object associated with the User object created above.
        self.cart = Cart.objects.create(user=self.user)

        # Create a Plant object
        self.plant = Plant.objects.create(name='Chamomile', price=12.20, image=self.create_valid_image())

        # Create a CartItem object associated with the Plant and Cart object created above.
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.plant)

        self.url = reverse('delete-cart-item', kwargs={'id': str(self.plant.id)}) # Get the URL endpoint


    def test_access_restriction_for_unauthenticated_user(self):
        """Make sure that an unauthenticated user cannot access the endpoint."""

        # MAKE a DELETE request to the delete-cart-item API endpoint
        response = self.client.delete(self.url)

        # Assert the status code is 403 (Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_cart_object_does_not_exist(self):
        """
        Make sure that the API endpoint correctly handles the case,
        when the Cart object is not found.
        """

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.user)

        # Make sure that the Cart object does not exist in the database
        self.cart.delete() # Remove the Cart object

        # Make a DELETE request to the delete-cart-item API endpoint
        response = self.client.delete(self.url)

        # Assert the status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_plant_object_does_not_exist(self):
        """
        Make sure that the API endpoint correctly handles the case,
        when the Cart object is not found.
        """

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.user)

        # Make sure that the Plant object does not exist in the database
        self.plant.delete() # Delete the Plant object

        # Make a DELETE request to the API endpoint.
        response = self.client.delete(self.url)

        # Assert the status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_cart_item_does_not_exist(self):
        """
        Make sure that the API endpoint correctly handles the case,
        when the CartItem object is not found.
        """

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.user)

        # Make sure that the CartItem object does not exist in the database
        self.cart_item.delete() # Delete the CartItem object

        # Make a DELETE request to the API endpoint
        response = self.client.delete(self.url)

        # Assert the status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_successful_deletion_of_cart_item(self):
        """Test successful deletion of the CartItem object."""

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.user)

        cart_item = CartItem

        # Make a DELETE request to the API endpoint
        response = self.client.delete(self.url)

        # Assert the status code is 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure the cart item has been deleted from the database
        self.assertEqual(self.cart.cart_items.all().count(), 0)



class IncreaseQuantityAPITest(FileUploadTestCase):
    """
    Test case for verifying the functionalities of the IncreaseQuantityAPITest endpoint.

    FileUploadTestCase is a custom base test case class that provides utility methods
    to handle file uploads in Django tests. It automates the setup of a temporary
    directory for storing uploaded files, ensuring that the `MEDIA_ROOT` is configured
    properly during the test. It also ensures that files are cleaned up and deleted
    after each test is run, preventing test pollution and improving isolation.

    Tests:
        - Test the endpoint restriction for unauthenticated users.
        - Test the behavior when the Cart object does not exist in the database.
        - Test the behavior when the Plant object does not exist in the database.
        - Test the behavior when the CartItem object does not exist in the database.
        - Test the successful increase in the quantity of the CartItem object.
    """

    def setUp(self):

        super().setUp() # Call the setUp of FileUploadTestCase to handle the media root setup

        # Initial the APIClient instance for testing
        self.client = APIClient() # Create a new instance of the APIClient

        # Create a regular User object
        self.user = User.objects.create_user(name='test', email='test@test.com', password='a12a14t56')

        # Create a Cart object associated with the User object created above.
        self.cart = Cart.objects.create(user=self.user)

        # Create a Plant object
        self.plant = Plant.objects.create(name='Chamomile', price=12.20, image=self.create_valid_image())

        # Create a CartItem object associated with the Plant and Cart object created above.
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.plant, quantity=1)

        self.url = reverse('increase-cart-item-quantity', kwargs={'id': str(self.plant.id)}) # Get the URL endpoint


    def test_access_restriction_for_unauthenticated_user(self):
        """Make sure that an unauthenticated user cannot access the endpoint."""

        # MAKE a Patch request to the increase-cart-item-quantity API endpoint
        response = self.client.patch(self.url)

        # Assert the status code is 403 (Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_cart_object_does_not_exist(self):
        """
        Make sure that the API endpoint correctly handles the case,
        when the Cart object is not found.
        """

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.user)

        # Make sure that the Cart object does not exist in the database
        self.cart.delete() # Remove the Cart object

        # Make a PATCH request to the increase-cart-item-quantity API endpoint
        response = self.client.patch(self.url)

        # Assert the status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_plant_object_does_not_exist(self):
        """
        Make sure that the API endpoint correctly handles the case,
        when the Cart object is not found.
        """

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.user)

        # Get the Plant object id before deleting it
        plant_id = self.plant.id

        # Make sure that the Plant object does not exist in the database
        self.plant.delete() # Delete the Plant object

        # Make a PATCH request to the API endpoint.
        response = self.client.patch(self.url)

        # Assert the status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_cart_item_does_not_exist(self):
        """
        Make sure that the API endpoint correctly handles the case,
        when the CartItem object is not found.
        """

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.user)

        # Make sure that the CartItem object does not exist in the database
        self.cart_item.delete() # Delete the CartItem object

        # Make a PATCH request to the API endpoint
        response = self.client.patch(self.url)

        # Assert the status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_cart_item_quantity_increase(self):
        """Test the successful increase in the quantity of the CartItem object."""

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.user)

        # Ensure the initial state of the cart item before update
        initial_quantity = self.cart_item.quantity

        # Make a PATCH request to the API endpoint
        response = self.client.patch(self.url)

        # Reload the cart item from the database to reflect any updates
        self.cart_item.refresh_from_db()

        # Make sure that the quantity was increased by 1
        self.assertEqual(self.cart_item.quantity, initial_quantity + 1)

        # Assert the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DecreaseQuantityAPITest(FileUploadTestCase):
    """
    Test case for verifying the functionalities of the DecreaseQuantityAPITest endpoint.

    FileUploadTestCase is a custom base test case class that provides utility methods
    to handle file uploads in Django tests. It automates the setup of a temporary
    directory for storing uploaded files, ensuring that the `MEDIA_ROOT` is configured
    properly during the test. It also ensures that files are cleaned up and deleted
    after each test is run, preventing test pollution and improving isolation.

    Tests:
        - Test the endpoint restriction for unauthenticated users.
        - Test the behavior when the Cart object does not exist in the database.
        - Test the behavior when the Plant object does not exist in the database.
        - Test the behavior when the CartItem object does not exist in the database.
        - Test the behavior when the quantity of the CartItem is equal to 1.
          It should remove the CartItem.
        - Test the successful decrease in the quantity of the CartItem object.
    """

    def setUp(self):

        super().setUp() # Call the setUp of FileUploadTestCase to handle the media root setup

        # Initial the APIClient instance for testing
        self.client = APIClient() # Create a new instance of the APIClient

        # Create a regular User object
        self.user = User.objects.create_user(name='test', email='test@test.com', password='a12a14t56')

        # Create a Cart object associated with the User object created above.
        self.cart = Cart.objects.create(user=self.user)

        # Create a Plant object
        self.plant = Plant.objects.create(name='Chamomile', price=12.20, image=self.create_valid_image())

        # Create a CartItem object associated with the Plant and Cart object created above.
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.plant, quantity=5)

        self.url = reverse('decrease-cart-item-quantity', kwargs={'id': str(self.plant.id)}) # Get the URL endpoint


    def test_access_restriction_for_unauthenticated_user(self):
        """Make sure that an unauthenticated user cannot access the endpoint."""

        # MAKE a Patch request to the decrease-cart-item-quantity API endpoint
        response = self.client.patch(self.url)

        # Assert the status code is 403 (Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_cart_object_does_not_exist(self):
        """
        Make sure that the API endpoint correctly handles the case,
        when the Cart object is not found.
        """

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.user)

        # Make sure that the Cart object does not exist in the database
        self.cart.delete() # Remove the Cart object

        # Make a PATCH request to the decrease-cart-item-quantity API endpoint
        response = self.client.patch(self.url)

        # Assert the status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_plant_object_does_not_exist(self):
        """
        Make sure that the API endpoint correctly handles the case,
        when the Cart object is not found.
        """

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.user)

        # Get the Plant object id before deleting it
        plant_id = self.plant.id

        # Make sure that the Plant object does not exist in the database
        self.plant.delete() # Delete the Plant object

        # Make a PATCH request to the API endpoint.
        response = self.client.patch(self.url)

        # Assert the status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_cart_item_does_not_exist(self):
        """
        Make sure that the API endpoint correctly handles the case,
        when the CartItem object is not found.
        """

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.user)

        # Make sure that the CartItem object does not exist in the database
        self.cart_item.delete() # Delete the CartItem object

        # Make a PATCH request to the API endpoint
        response = self.client.patch(self.url)

        # Assert the status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_remove_cart_item_when_quantity_is_one(self):
        """Test that the CartItem is removed when its quantity is equal to 1."""

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.user)

        # Make sure that the CartItem's quantity is equal to one.
        self.cart_item.quantity = 1
        self.cart_item.save() # Save object

        # Make a PATCH request to the API endpoint
        response = self.client.patch(self.url)

        # Assert the status_code is 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Assert the CartItem object was deleted
        self.assertEqual(self.cart.cart_items.all().count(), 0)


    def test_cart_item_quantity_decrease(self):
        """Test the successful increase in the quantity of the CartItem object."""

        # Login user to avoid access restrictions
        self.client.force_authenticate(user=self.user)

        # Ensure the initial state of the cart item before update
        initial_quantity = self.cart_item.quantity

        # Make a PATCH request to the API endpoint
        response = self.client.patch(self.url)

        # Reload the cart item from the database to reflect any updates
        self.cart_item.refresh_from_db()

        # Make sure that the quantity was decreased by 1
        self.assertEqual(self.cart_item.quantity, initial_quantity - 1)

        # Assert the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)