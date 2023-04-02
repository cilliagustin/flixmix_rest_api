from rest_framework import generics, permissions
from flixmix_rest_api.permissions import IsOwnerOrReadOnly
from .models import Seen
from .serializers import SeenSerializer


class SeenList(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    serializer_class = SeenSerializer
    queryset = Seen.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SeenDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = SeenSerializer
    queryset = Seen.objects.all()
