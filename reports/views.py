from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from flixmix_rest_api.permissions import IsAdminOrReadOnly
from .models import Report
from .serializers import ReportSerializer


class ReportList(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Report.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['is_closed', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by is_closed
        is_closed = self.request.query_params.get('is_closed', None)
        if is_closed is not None:
            is_closed = is_closed.lower() == 'true'
            queryset = queryset.filter(is_closed=is_closed)

        # Filter by movie_title
        movie_title = self.request.query_params.get('movie_title', None)
        if movie_title is not None:
            queryset = queryset.filter(movie__title__icontains=movie_title)

        # Filter by Owner Username
        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            queryset = queryset.filter(owner__username__icontains=owner)

        # Order by is_closed (false first) and then by created_at
        queryset = queryset.order_by('is_closed', '-created_at')

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
