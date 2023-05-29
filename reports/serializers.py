from django.db import IntegrityError
from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    """
    Serializer for the report.
    Provides owners information (id, image and username).
    Provides movie information (id, image title and release year).
    Raises an error if the user tries to report a movie they already have
    reported.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    movie_title = serializers.ReadOnlyField(source='movie.title')
    movie_release_year = serializers.ReadOnlyField(source='movie.release_year')
    movie_poster = serializers.ReadOnlyField(source='movie.poster.url')

    class Meta:
        model = Report
        fields = [
            'id', 'owner', 'profile_id', 'profile_image', 'movie',
            'movie_title', 'movie_release_year', 'movie_poster', 'content',
            'created_at',
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'You already reported an error in this movie!'
            })
