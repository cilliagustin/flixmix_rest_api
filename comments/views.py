from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from flixmix_rest_api.permissions import IsOwnerOrAdminOrReadOnly
from .models import RatingComment, ListComment
from .serializers import (
    ListCommentSerializer,
    ListCommentDetailSerializer,
    RatingCommentSerializer,
    RatingCommentDetailSerializer
)


class ListCommentList(generics.ListCreateAPIView):
    serializer_class = ListCommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = ListComment.objects.all()
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'list',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = ListCommentDetailSerializer
    queryset = ListComment.objects.all()


class RatingCommentList(generics.ListCreateAPIView):
    serializer_class = RatingCommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = RatingComment.objects.all()
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'rating',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RatingCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = RatingCommentDetailSerializer
    queryset = RatingComment.objects.all()
