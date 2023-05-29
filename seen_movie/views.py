from rest_framework import generics, permissions
from flixmix_rest_api.permissions import IsOwnerOrReadOnly
from .models import Seen
from .serializers import SeenSerializer
from watchlist.models import Watchlist


class SeenList(generics.ListCreateAPIView):
    """
    List of seen movies. Without log in status only has reading permissions.
    When the user creates a seen movie is this is in their watchlist it
    deletes the watchlist instance.
    """
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
    """
    Detail of the seen movie. Without the admin status or owner status the
    user only has reading permissions.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = SeenSerializer
    queryset = Seen.objects.all()
