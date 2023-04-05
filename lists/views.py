from django.db.models import Count
from rest_framework import generics, permissions, filters
from flixmix_rest_api.permissions import IsOwnerOrAdminOrReadOnly
from .models import List
from .serializers import ListSerializer


class ListList(generics.ListCreateAPIView):
    serializer_class = ListSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = List.objects.annotate(
        comments_count=Count('listcomment', distinct=True),
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        'title',
        'movies__title',
    ]
    ordering_fields = [
        'comments_count',
    ]

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
    queryset = List.objects.annotate(
        comments_count=Count('listcomment', distinct=True),
    ).order_by('-created_at')
