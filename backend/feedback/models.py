from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from account.models import User

import uuid

# Create your models here.


class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    content = models.TextField(max_length=800)
    rating = models.PositiveIntegerField()
    added_at = models.DateTimeField(default=timezone.now)


    class Meta:
        constraints = [
            models.CheckConstraint(
                check = models.Q(rating__gte=0, rating__lte=5), # Rating must be between 0 and 5 (inclusive)
                name = 'rating_between_0_and_5'
            )
        ]


    def __str__(self):
        """Returns a human-readable string representation of the Feedback object."""
        return self.content[:20].strip()


    def clean(self):
        """Validates the model fields"""

        self.content = self.content.strip() # Strip leading/trailing spaces from the content field

        # Make sure that the length of the content field is between 20 and 800 characters.
        if len(self.content) < 20 or len(self.content) > 800:
            raise ValidationError('The content field must include between 20 and 800 characters.')

        # Make sure that the rating field is positive and less than or equal to five.
        if self.rating < 0 or self.rating > 5:
            raise ValidationError('The rating field must be between 0 and 5 (inclusive)')


    def save(self, *args, **kwargs):
        """Ensure that the 'clean' method is called before the object instance is saved."""

        self.clean() # Call the clean method
        super().save(*args, **kwargs)