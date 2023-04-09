from django.db.models import Count, F, ExpressionWrapper, IntegerField
from rest_framework import status, permissions, filters
from django.http import Http404
from rest_framework import generics
from .models import Movie
from .serializers import MovieSerializer
from flixmix_rest_api.permissions import IsAdminOrReadOnly


class MovieList(generics.ListCreateAPIView):
    """
    List movies or create if logged in
    """
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Movie.objects.annotate(
        seen_count=Count('seen', distinct=True),
        watchlist_count=Count('watchlist', distinct=True),
        list_count=Count('lists', distinct=True),
        rating_count=Count('rating', distinct=True),
        release_decade=ExpressionWrapper(
            F('release_year') - F('release_year') % 10,
            output_field=IntegerField()
        )
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        'title',
        'directors',
        'main_cast',
        'release_decade',
    ]
    ordering_fields = [
        'seen_count',
        'watchlist_count',
        'list_count',
        'rating_count',
        'watchlist__created_at',
        'seen__created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a movie, only admins can edit it.
    """
    serializer_class = MovieSerializer
    # Only the admin can edit/delete a movie
    permission_classes = [IsAdminOrReadOnly]
    queryset = Movie.objects.annotate(
        seen_count=Count('seen', distinct=True),
        watchlist_count=Count('watchlist', distinct=True),
        list_count=Count('lists', distinct=True),
        rating_count=Count('rating', distinct=True),
    ).order_by('-created_at')
