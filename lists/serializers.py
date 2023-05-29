from rest_framework import serializers
from .models import List
from movies.models import Movie


"""
Movie serializer to provide movie information in the list.
Provides the movie id, title, poster and release year.
"""


class MovieDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'poster', 'release_year']


"""
Serializer for the list.
Provides owners information (id, image and username).
Gets the comment count provided by the views.
Gets the movie detaiuls from the MovieDetailsSerializer.
"""


class ListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    comments_count = serializers.ReadOnlyField()
    movies_details = MovieDetailsSerializer(
        many=True, read_only=True, source='movies')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = List
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'title', 'description',
            'movies', 'movies_details', 'comments_count'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']
