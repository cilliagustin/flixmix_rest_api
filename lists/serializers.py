from rest_framework import serializers
from .models import List
from movies.serializers import MovieSerializer


class ListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    # movies = MovieSerializer(many=True, read_only=True)
    comments_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = List
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'title', 'description',
            'movies', 'comments_count'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']

    # def create(self, validated_data):
    #     movie_data = validated_data.pop('movies')
    #     instance = List.objects.create(**validated_data)
    #     for movie in movie_data:
    #         instance.movies.add(movie['id'])
    #     return instance

    # def update(self, instance, validated_data):
    #     movie_data = validated_data.pop('movies', [])
    #     if movie_data:
    #         movie_serializer = MovieSerializer(many=True, data=movie_data)
    #         movie_serializer.is_valid(raise_exception=True)
    #         movie_objects = movie_serializer.save()
    #         instance.movies.set(movie_objects)
    #     instance = super().update(instance, validated_data)
    #     return instance
