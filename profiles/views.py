from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile
from .serializers import ProfileSerializer
from flixmix_rest_api.permissions import IsOwnerOrAdminOrReadOnly


class ProfileList(generics.ListAPIView):
    # Only list profiles (creation is done with signals)
    queryset = Profile.objects.annotate(
        movie_count=Count('owner__movie', distinct=True),
        seen_count=Count('owner__seen', distinct=True),
        watchlist_count=Count('owner__watchlist', distinct=True),
        list_count=Count('owner__list', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'movie__count',
        'seen__count',
        'watchlist__count',
        'list__count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    # Retrieve or update data if user is owner or admin
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    queryset = Profile.objects.annotate(
        movie_count=Count('owner__movie', distinct=True),
        seen_count=Count('owner__seen', distinct=True),
        watchlist_count=Count('owner__watchlist', distinct=True),
        list_count=Count('owner__list', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
