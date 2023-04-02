from rest_framework import status, permissions
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
    queryset = Movie.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a movie, only admins can edit it.
    """
    serializer_class = MovieSerializer
    # Only the admin can edit/delete a movie
    permission_classes = [IsAdminOrReadOnly]
    queryset = Movie.objects.all()
