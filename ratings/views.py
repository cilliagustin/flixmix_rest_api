from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from flixmix_rest_api.permissions import IsOwnerOrAdminOrReadOnly
from .models import Rating
from .serializers import RatingSerializer, RatingDetailSerializer
from watchlist.models import Watchlist
from seen_movie.models import Seen


class RatingList(generics.ListCreateAPIView):
    """
    Detail of the movie. Without log in status only has reading permissions.
    Provides the ammount of comments the rating has.
    Provides filtering for the movie and owner a user follows.
    Provides custom search fields for movie title, owner username, owner id.
    """
    serializer_class = RatingSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Rating.objects.annotate(
        comments_count=Count('ratingcomment', distinct=True),
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'movie',
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'comments_count',
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by Movie title
        movie_title = self.request.query_params.get('movie_title', None)
        if movie_title is not None:
            queryset = queryset.filter(movie__title__icontains=movie_title)

        # Filter by Owner Username
        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            queryset = queryset.filter(owner__username__icontains=owner)

        # Filter by Owner ID
        owner_id = self.request.query_params.get('owner_id', None)
        if owner_id is not None:
            queryset = queryset.filter(owner__id=owner_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail of rating. If the user is not the owner or admin
    they only have reading permissions.
    Provides the ammount of comments the list has.
    """
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = RatingDetailSerializer
    queryset = Rating.objects.annotate(
        comments_count=Count('ratingcomment', distinct=True),
    ).order_by('-created_at')
