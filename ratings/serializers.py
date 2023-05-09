
from django.db import IntegrityError
from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    movie_title = serializers.ReadOnlyField(source='movie.title')
    comments_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Rating
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image', 'movie',
            'movie_title', 'value', 'title', 'content', 'created_at', 
            'updated_at', 'comments_count'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'You have already rated this movie.'
            })


class RatingDetailSerializer(RatingSerializer):
    movie = serializers.ReadOnlyField(source='movie.id')
