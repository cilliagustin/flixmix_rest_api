from django.db import IntegrityError
from rest_framework import serializers
from .models import Seen


class SeenSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    movie_title = serializers.ReadOnlyField(source='movie.title')

    class Meta:
        model = Seen
        fields = [
            'id', 'owner', 'movie', 'movie_title', 'created_at'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate!'
            })