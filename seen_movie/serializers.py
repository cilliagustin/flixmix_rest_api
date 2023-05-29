from django.db import IntegrityError
from rest_framework import serializers
from .models import Seen


class SeenSerializer(serializers.ModelSerializer):
    """
    Serializer for the seen movie.
    Provides the movie title.
    Raises an error if the user tries to mark a movie as seen that they
    already have marked as that.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    movie_title = serializers.ReadOnlyField(source='movie.title')

    class Meta:
        model = Seen
        fields = [
            'id', 'owner', 'movie', 'movie_title', 'created_at'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'Yoy have already marked this movie as seen!'
            })
