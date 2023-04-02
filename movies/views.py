from rest_framework import status, permissions
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieSerializer
from flixmix_rest_api.permissions import IsAdminOrReadOnly


class MovieList(APIView):
    serializer_class = MovieSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(
            movies, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class MovieDetail(APIView):
    serializer_class = MovieSerializer
    # Only the admin can edit/delete a movie
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            return movie
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        movie = self.get_object(pk)
        self.check_object_permissions(self.request, movie)
        serializer = MovieSerializer(
            movie, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        movie = self.get_object(pk)
        serializer = MovieSerializer(
            movie, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        movie = self.get_object(pk)
        movie.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
