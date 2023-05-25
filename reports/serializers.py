from django.db import IntegrityError
from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    movie_title = serializers.ReadOnlyField(source='movie.title')
    movie_release_year = serializers.ReadOnlyField(source='movie.release_year')
    movie_poster = serializers.ReadOnlyField(source='movie.poster.url')

    class Meta:
        model = Report
        fields = [
            'id', 'owner', 'profile_id', 'profile_image', 'movie',
            'movie_title', 'movie_release_year', 'movie_poster', 'content',
            'created_at', 'updated_at', 'is_closed'
        ]

    def create(self, validated_data):
        owner = self.context['request'].user
        movie = validated_data['movie']

        # Check if the user has already reported the movie
        existing_reports = Report.objects.filter(owner=owner, movie=movie)

        for report in existing_reports:
            if report.is_closed:
                # Delete the previous closed report
                report.delete()
            else:
                raise serializers.ValidationError({
                    'detail': 'You have already reported this movie.'
                })

        # Create a new report
        return super().create(validated_data)
