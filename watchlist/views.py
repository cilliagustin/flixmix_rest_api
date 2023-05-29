from rest_framework import generics, permissions
from flixmix_rest_api.permissions import IsOwnerOrReadOnly
from .models import Watchlist
from .serializers import WatchlistSerializer
from seen_movie.models import Seen
from ratings.models import Rating


class WatchlistList(generics.ListCreateAPIView):
    """
    List of movies in the watchlist. Without log in status only has reading
    permissions.
    When the user creates a watchlist movie is this is marked as seen it
    deletes the seen instance.
    """
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    serializer_class = WatchlistSerializer
    queryset = Watchlist.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        movie = serializer.validated_data['movie']

        # Check if the movie is already in the seen list for the user
        try:
            seen = Seen.objects.get(owner=user, movie=movie)
            # In that case, delete it from the seen list and add it to the
            # watchlist instead
            seen.delete()
        except Seen.DoesNotExist:
            pass

        serializer.save(owner=user)


class WatchlistDetailView(generics.RetrieveDestroyAPIView):
    """
    Detail of the watchlist. Without the admin status or owner status the
    user only has reading permissions.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = WatchlistSerializer
    queryset = Watchlist.objects.all()
