from rest_framework import generics, permissions
from flixmix_rest_api.permissions import IsOwnerOrAdminOrReadOnly
from .models import List
from .serializers import ListSerializer


class ListList(generics.ListCreateAPIView):
    serializer_class = ListSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = List.objects.all()

    def perform_create(self, serializer):
        data = self.request.data.copy()
        movies_data = data.pop('movies', [])
        list_instance = serializer.save(owner=self.request.user)

        movie_instances = []
        for movie in movies_data:
            movie_instance = Movie.objects.get(pk=movie['id'])
            movie_instances.append(movie_instance)

        list_instance.movies.set(movie_instances)

    def get_serializer(self, *args, **kwargs):
        if 'data' in kwargs:
            data = kwargs['data']
            if isinstance(data, list):
                kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)


class ListDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = ListSerializer
    queryset = List.objects.all()