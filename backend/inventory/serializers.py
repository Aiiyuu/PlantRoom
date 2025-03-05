from rest_framework.serializers import ModelSerializer
from .models import Plant


class PlantSerializer(ModelSerializer):
    """Serializer for the Plant model."""
    
    class Meta:
        model=Plant
        fields='__all__'