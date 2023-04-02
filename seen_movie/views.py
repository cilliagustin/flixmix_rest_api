from rest_framework import generics, permissions
from flixmix_rest_api.permissions import IsOwnerOrReadOnly
from .models import Seen
from .serializers import SeenSerializer
from watchlist.models import Watchlist


class SeenList(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    serializer_class = SeenSerializer
    queryset = Seen.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        movie = serializer.validated_data['movie']
        try:
            # Check if the movie is already in the watchlist for the user
            watchlist = Watchlist.objects.get(owner=user, movie=movie)
            # In that case, delete it from the watchlist and add it to the
            # seen list instead
            watchlist.delete()
            serializer.save(owner=user)
        except Watchlist.DoesNotExist:
            serializer.save(owner=user)


class SeenDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = SeenSerializer
    queryset = Seen.objects.all()
