from rest_framework import generics, permissions
from flixmix_rest_api.permissions import IsOwnerOrAdminOrReadOnly
from .models import Rating
from .serializers import RatingSerializer, RatingDetailSerializer


class RatingList(generics.ListCreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Rating.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = RatingDetailSerializer
    queryset = Rating.objects.all()
