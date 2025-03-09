from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """The UserSerializer serializers data and converts it into a JSON format."""

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'date_joined', 'is_superuser']