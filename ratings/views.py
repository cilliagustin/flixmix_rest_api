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
        movie_id = serializer.validated_data['movie'].id
        user_id = self.request.user.id

        # Check if the user has already rated this movie
        if Rating.objects.filter(movie_id=movie_id, owner_id=user_id).exists():
            # If rating exists, update the existing rating instead of
            # creating a new one
            existing_rating = Rating.objects.get(
                movie_id=movie_id, owner_id=user_id
            )
            serializer.instance = existing_rating
            serializer.update(existing_rating, serializer.validated_data)
        else:
            # Otherwise, create a new rating
            serializer.save(owner=self.request.user)


class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = RatingDetailSerializer
    queryset = Rating.objects.all()
