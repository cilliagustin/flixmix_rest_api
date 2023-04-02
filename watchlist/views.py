from rest_framework import generics, permissions
from flixmix_rest_api.permissions import IsOwnerOrReadOnly
from .models import Watchlist
from .serializers import WatchlistSerializer


class WatchlistList(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    serializer_class = WatchlistSerializer
    queryset = Watchlist.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WatchlistDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = WatchlistSerializer
    queryset = Watchlist.objects.all()
