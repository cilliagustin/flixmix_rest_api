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
        serializer.save(owner=self.request.user)


class ListDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = ListSerializer
    queryset = List.objects.annotate(
        comments_count=Count('listcomment', distinct=True),
    ).order_by('-created_at')
