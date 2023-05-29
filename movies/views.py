from django.db.models import Count, F, ExpressionWrapper, IntegerField
from rest_framework import status, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from rest_framework import generics
from .models import Movie
from .serializers import MovieSerializer
from flixmix_rest_api.permissions import IsAdminOrReadOnly


class MovieList(generics.ListCreateAPIView):
    """
    List of Movies. Without log in status only has reading permissions.
    Provides the ammount of times the movie was marked as seen.
    Provides the ammount of times the movie was added to a watchlist.
    Provides the ammount of times the movie was rated.
    Provides the ammount of times the movie appears on a list.
    Provides the ammount of reports the movie has.
    Gets the release decade from the release year.
    Has a search field for the movie title.
    Provides filtering for the owner, owners a user follows, movies a profile
    marked as seen, movies a profile added to a watchlist.
    Provides custom search fields for movie title, director, main cast,
    release decade and owner id.
    """
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Movie.objects.annotate(
        seen_count=Count('seen', distinct=True),
        watchlist_count=Count('watchlist', distinct=True),
        list_count=Count('lists', distinct=True),
        rating_count=Count('rating', distinct=True),
        report_count=Count('report', distinct=True),
        release_decade=ExpressionWrapper(
            F('release_year') - F('release_year') % 10,
            output_field=IntegerField()
        )
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'seen__owner__profile',
        'watchlist__owner__profile',
        'owner__profile',
    ]
    ordering_fields = [
        'seen_count',
        'watchlist_count',
        'list_count',
        'rating_count',
        'watchlist__created_at',
        'seen__created_at',
        'report_count',
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by title
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)

        # Filter by director
        directors = self.request.query_params.get('directors', None)
        if directors is not None:
            queryset = queryset.filter(directors__icontains=directors)

        # Filter by main cast
        main_cast = self.request.query_params.get('main_cast', None)
        if main_cast is not None:
            queryset = queryset.filter(main_cast__icontains=main_cast)

        # Filter by release decade
        release_decade = self.request.query_params.get('release_decade', None)
        if release_decade is not None:
            queryset = queryset.filter(release_decade=release_decade)

        # Filter by owner (creator) ID
        owner_id = self.request.query_params.get('owner_id', None)
        if owner_id is not None:
            queryset = queryset.filter(owner__id=owner_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail of the movie. If the user is not the admin they only have reading
    permissions.
    Comments are filtered by lists.
    Provides the ammount of times the movie was marked as seen.
    Provides the ammount of times the movie was added to a watchlist.
    Provides the ammount of times the movie was rated.
    Provides the ammount of times the movie appears on a list.
    Provides the ammount of reports the movie has.
    Gets the release decade from the release year.
    """
    serializer_class = MovieSerializer
    # Only the admin can edit/delete a movie
    permission_classes = [IsAdminOrReadOnly]
    queryset = Movie.objects.annotate(
        seen_count=Count('seen', distinct=True),
        watchlist_count=Count('watchlist', distinct=True),
        list_count=Count('lists', distinct=True),
        rating_count=Count('rating', distinct=True),
        report_count=Count('report', distinct=True),
        release_decade=ExpressionWrapper(
            F('release_year') - F('release_year') % 10,
            output_field=IntegerField()
        )
    ).order_by('-created_at')
