from django.db import IntegrityError
from rest_framework import serializers
from .models import Watchlist


class WatchlistSerializer(serializers.ModelSerializer):
    """
    Serializer for the watchlist.
    Provides the movie title.
    Raises an error if the user tries to mark a movie as a future watch that
    they already have marked as that.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    movie_title = serializers.ReadOnlyField(source='movie.title')

    class Meta:
        model = Watchlist
        fields = [
            'id', 'owner', 'movie', 'movie_title', 'created_at'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'You have already added this movie to your watchlist'
            })
