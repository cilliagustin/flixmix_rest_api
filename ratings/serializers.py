from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    movie_title = serializers.ReadOnlyField(source='movie.title')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Rating
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'movie', 'movie_title',
            'value', 'review', 'created_at', 'updated_at',
        ]


class RatingDetailSerializer(RatingSerializer):
    movie = serializers.ReadOnlyField(source='movie.id')
