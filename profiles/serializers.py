from rest_framework import serializers
from .models import Profile
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the profile.
    Gets the is admin field by the model.
    Gets the movie count, seen count, watchlist count, list count,
    rating count follower count and following count provided by the views.
    Gets the following id if it exist.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    movie_count = serializers.ReadOnlyField()
    seen_count = serializers.ReadOnlyField()
    watchlist_count = serializers.ReadOnlyField()
    list_count = serializers.ReadOnlyField()
    rating_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'description', 'image', 'is_admin',
            'is_owner', 'following_id', 'movie_count', 'seen_count',
            'rating_count', 'watchlist_count', 'list_count',
            'followers_count', 'following_count'
        ]
