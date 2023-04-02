from rest_framework import generics, permissions
from flixmix_rest_api.permissions import IsOwnerOrReadOnly
from .models import Watchlist
from .serializers import WatchlistSerializer
from seen_movie.models import Seen


class WatchlistList(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    serializer_class = WatchlistSerializer
    queryset = Watchlist.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        movie = serializer.validated_data['movie']
        try:
            # Check if the movie is already in the seen list for the user
            seen = Seen.objects.get(owner=user, movie=movie)
            # In that case, delete it from the seen list and add it to the
            # watchlist instead
            seen.delete()
            serializer.save(owner=user)
        except Seen.DoesNotExist:
            serializer.save(owner=user)


class WatchlistDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = WatchlistSerializer
    queryset = Watchlist.objects.all()
