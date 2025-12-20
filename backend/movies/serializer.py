from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for the Movie model.
    Validates that the rating is between 0.0 and 5.0. and serializes all fields.
    """
    rating = serializers.FloatField(min_value=0.0, max_value=5.0)

    class Meta:
        model = Movie
        fields = "__all__"