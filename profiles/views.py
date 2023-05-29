from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile
from .serializers import ProfileSerializer
from flixmix_rest_api.permissions import IsOwnerOrAdminOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    Only list profiles (creation is done with signals)
    Comments are filtered by lists.
    Provides the ammount of times the user movie marked a movie as seen.
    Provides the ammount of times the user movie marked a movie as a future
    watch.
    Provides the ammount of times the user movie rated a movie.
    Provides the ammount of times the user movie created a list.
    Provides the ammount of profiles the user follows.
    Provides the ammount of profiles the user is followed by.
    Provides filtering for the profiles a user follows and profiles that
    follow a user.
    """
    queryset = Profile.objects.annotate(
        movie_count=Count('owner__movie', distinct=True),
        seen_count=Count('owner__seen', distinct=True),
        watchlist_count=Count('owner__watchlist', distinct=True),
        rating_count=Count('owner__rating', distinct=True),
        list_count=Count('owner__list', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    search_fields = [
        'owner__username',
        'name',
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
    """
    Detail of the profile. If the user is not the admin or the profile they
    only have reading permissions.
    Provides the ammount of times the user uploaded movie.
    Provides the ammount of times the user movie marked a movie as seen.
    Provides the ammount of times the user movie marked a movie as a future
    watch.
    Provides the ammount of times the user movie rated a movie.
    Provides the ammount of times the user movie created a list.
    Provides the ammount of profiles the user follows.
    Provides the ammount of profiles the user is followed by.
    """
    # Retrieve or update data if user is owner or admin
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    queryset = Profile.objects.annotate(
        movie_count=Count('owner__movie', distinct=True),
        seen_count=Count('owner__seen', distinct=True),
        watchlist_count=Count('owner__watchlist', distinct=True),
        rating_count=Count('owner__rating', distinct=True),
        list_count=Count('owner__list', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
