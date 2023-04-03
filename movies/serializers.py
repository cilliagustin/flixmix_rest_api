from rest_framework import serializers
from .models import Movie
from seen_movie.models import Seen


class MovieSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    avg_rating = serializers.SerializerMethodField()
    release_decade = serializers.ReadOnlyField()
    seen_count = serializers.SerializerMethodField()
    poster = serializers.ImageField(required=False)
    seen_id = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_avg_rating(self, obj):
        return obj.avg_rating()

    def get_seen_count(self, obj):
        return obj.seen_count()

    def get_watchlist_count(self, obj):
        return obj.watchlist_count()

    def get_seen_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            seen = Seen.objects.filter(
                owner=user, movie=obj
            ).first()
            return seen.id if seen else None
        return None

    def validate_poster(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        # make sure the image has a 2:3 ratio
        # (width aproximately 70% of height)
        if (
            value.image.width < (value.image.height * .60) or
            value.image.width > (value.image.height * .80)
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
            'poster', 'release_year', 'release_decade', 'movie_genre',
            'avg_rating', 'seen_count', 'watchlist_count', 'seen_id'
        ]
