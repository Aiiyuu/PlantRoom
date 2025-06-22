import os
import tempfile
import shutil

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class FileUploadTestCase(TestCase):
    """
    A base test case class for handling file uploads in Django tests.
    
    This class sets up a temporary directory for storing uploaded files during
    the tests.
    
    Usage:
        - Inherit from this class in your test class
        - Use the 'create_valid_image' method to generate an image in one 
            of the following formats: PNG, JPEG, or JPG.
        - Use the 'create_invalid_format_image' method to generate an image 
            in an incorrect format (in this case, GIF).
        - Use the 'create_large_image' method to generate an image file of 15MB.
        - The test's `MEDIA_ROOT` will be automatically handled and cleaned up
          after each test.
    """
    
    
    def setUp(self):
        # Create a temporary directory for storing uploaded files
        self.test_media_dir = tempfile.mkdtemp()
        
        # Set the MEDIA_ROOT for the test to point to this temporary file.
        self.old_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = self.test_media_dir
        
    
    def tearDown(self):
        """Clean up all files in the test MEDIA_ROOT."""
        
        # Remove the temporary directory and its contents
        for filename in os.listdir(self.test_media_dir):
            # Construct the full file path by joining the directory path with the file name
            file_path = os.path.join(self.test_media_dir, filename)
            
            # Check if the current file path refers to a file (not a directory)
            if os.path.isfile(file_path):
                # If it's a file, delete it using os.unlink(), which removes a single file
                os.unlink(file_path)
                
                
        # After cleaning up files, remove the temporary directory
        shutil.rmtree(self.test_media_dir)
        
        
    def create_valid_image(self, name="test_image.jpg", content=b"fake_image_data"):
        """Helper method to create a valid image."""
        
        return SimpleUploadedFile(name, content, content_type="image/jpeg")
    
    
    def create_invalid_image(self, name="test_image.gif", content=b"fake_image_data"):
        """Helper method to create an invalid image (in this case, in GIF format)."""
        
        return SimpleUploadedFile(name, content, content_type="image/gif")
    
    
    def create_large_image(self, name="test_image.jpg", content=b"fake_image_data"):
        """Helper method to create a large image (in this case, a 15MB file)."""
        
        size_mb = 15 # Simulate 15 MB
        content = b"0" * (size_mb * 1024 * 1024)  # Create a raw binary string of 'size_mb' MB
        
        return SimpleUploadedFile(name, content, content_type="image/jpg")