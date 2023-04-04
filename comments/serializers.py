from rest_framework import serializers
from .models import RatingComment, ListComment


class BaseCommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        abstract = True
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'created_at',
            'updated_at', 'content',
        ]


class ListCommentSerializer(BaseCommentSerializer):

    class Meta(BaseCommentSerializer.Meta):
        model = ListComment
        fields = BaseCommentSerializer.Meta.fields + ['list']


class ListCommentDetailSerializer(ListCommentSerializer):
    list_id = serializers.ReadOnlyField(source='list.id')

    class Meta(ListCommentSerializer.Meta):
        fields = ListCommentSerializer.Meta.fields + ['list_id']


class RatingCommentSerializer(BaseCommentSerializer):

    class Meta(BaseCommentSerializer.Meta):
        model = RatingComment
        fields = BaseCommentSerializer.Meta.fields + ['rating']


class RatingCommentDetailSerializer(RatingCommentSerializer):
    rating_id = serializers.ReadOnlyField(source='rating.id')

    class Meta(RatingCommentSerializer.Meta):
        fields = RatingCommentSerializer.Meta.fields + ['rating_id']
