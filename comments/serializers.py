from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import RatingComment, ListComment


class BaseCommentSerializer(serializers.ModelSerializer):
    """
    Basic serializer for comment, the ListCommentSerializer and
    RatingCommentSerializer will inherit from here.
    Also provides owners information (id, image and username)
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        abstract = True
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'content',
        ]


class ListCommentSerializer(BaseCommentSerializer):
    """
    Inherits from BaseCommentSerializer and adds the model and the field list
    """
    class Meta(BaseCommentSerializer.Meta):
        model = ListComment
        fields = BaseCommentSerializer.Meta.fields + ['list']


class ListCommentDetailSerializer(ListCommentSerializer):
    """
    Inherits from ListCommentSerializer and adds the list id
    """
    list_id = serializers.ReadOnlyField(source='list.id')

    class Meta(ListCommentSerializer.Meta):
        fields = ListCommentSerializer.Meta.fields + ['list_id']


class RatingCommentSerializer(BaseCommentSerializer):
    """
    Inherits from BaseCommentSerializer and adds the model and the field rating
    """
    class Meta(BaseCommentSerializer.Meta):
        model = RatingComment
        fields = BaseCommentSerializer.Meta.fields + ['rating']


class RatingCommentDetailSerializer(RatingCommentSerializer):
    """
    Inherits from RatingCommentDetailSerializer and adds the rating id
    """
    rating_id = serializers.ReadOnlyField(source='rating.id')

    class Meta(RatingCommentSerializer.Meta):
        fields = RatingCommentSerializer.Meta.fields + ['rating_id']
