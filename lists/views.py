from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from flixmix_rest_api.permissions import IsOwnerOrAdminOrReadOnly
from .models import List
from .serializers import ListSerializer

"""
List of lists. Without log in status only has reading permissions.
Provides the ammount of comments the list has.
Has a search field for the movie title.
Provides filtering for the owner and owner a user follows.
Provides custom search fields for list title, owner username, owner id.
"""


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
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'owner__profile',
    ]
    search_fields = [
        'movies__title',
    ]
    ordering_fields = [
        'comments_count',
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by List title
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)

        # Filter by Owner Username
        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            queryset = queryset.filter(owner__username__icontains=owner)

        # Filter by owner (creator) ID
        owner_id = self.request.query_params.get('owner_id', None)
        if owner_id is not None:
            queryset = queryset.filter(owner__id=owner_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


"""
Detail of lists. If the user is not the owner or admin
they only have reading permissions.
Comments are filtered by lists.
Provides the ammount of comments the list has.
"""


class ListDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = ListSerializer
    queryset = List.objects.annotate(
        comments_count=Count('listcomment', distinct=True),
    ).order_by('-created_at')
