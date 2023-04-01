from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    avg_rating = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_avg_rating(self, obj):
        return obj.avg_rating()

    def validate_poster(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.poster.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.poster.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        # make sure the image has a 2:3 ratio
        # (width aproximately 70% of height)
        if (
            value.poster.width < (value.poster.height * .60) or
            value.poster.width > (value.poster.height * .80)
        ):
            raise serializers.ValidationError(
                'Poster images have an aproximate ratio of 2:3!'
            )
        return value

    class Meta:
        model = Movie
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'created_at', 
            'updated_at', 'title', 'synopsis', 'directors', 'main_cast', 
            'poster', 'release_year', 'movie_genre', 'avg_rating'
        ]