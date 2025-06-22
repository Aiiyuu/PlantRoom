from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Plant


class PlantSerializer(ModelSerializer):
    """Serializer for the Plant model."""

    # Declare custom fields
    discounted_price = SerializerMethodField()
    in_stock = SerializerMethodField()
    
    class Meta:
        model=Plant
        fields='__all__'

    def get_discounted_price(self, obj):
        """Return the discounted price of the plant."""
        return obj.get_discounted_price()

    def get_in_stock(self, obj):
        """Return whether the plant is in stock."""
        return obj.in_stock