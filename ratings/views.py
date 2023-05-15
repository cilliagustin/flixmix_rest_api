from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from flixmix_rest_api.permissions import IsOwnerOrAdminOrReadOnly
from .models import Rating
from .serializers import RatingSerializer, RatingDetailSerializer
from watchlist.models import Watchlist
from seen_movie.models import Seen


class RatingList(generics.ListCreateAPIView):
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

        # Filter by Creator
        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            queryset = queryset.filter(owner__username__icontains=owner)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        movie = serializer.validated_data['movie']

        try:
            # Check if the movie is in the user's watchlist
            watchlist = Watchlist.objects.get(owner=user, movie=movie)
            watchlist.delete()

            # Check if the movie is marked as seen by the user
            seen = Seen.objects.filter(owner=user, movie=movie).exists()
            if not seen:
                # If not, mark it as seen
                Seen.objects.create(owner=user, movie=movie)

        except Watchlist.DoesNotExist:
            pass

        serializer.save(owner=user)


class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = RatingDetailSerializer
    queryset = Rating.objects.annotate(
        comments_count=Count('ratingcomment', distinct=True),
    ).order_by('-created_at')
