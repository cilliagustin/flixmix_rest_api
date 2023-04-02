from rest_framework import serializers
from .models import Director, Actor


class CrewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Crew model (abstract base class).
    """

    class Meta:
        model = Director
        fields = [
            'id', 'crew_name'
        ]


class DirectorSerializer(CrewSerializer):
    """
    Serializer for the Director model.
    """

    class Meta(CrewSerializer.Meta):
        model = Director


class ActorSerializer(CrewSerializer):
    """
    Serializer for the Actor model.
    """

    class Meta(CrewSerializer.Meta):
        model = Actor
