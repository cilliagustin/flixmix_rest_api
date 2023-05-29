from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from flixmix_rest_api.permissions import IsAdminOrReadOnly
from .models import Report
from .serializers import ReportSerializer


class ReportList(generics.ListCreateAPIView):
    """
    List of report. Without log in status only has reading permissions.
    Provides custom search fields for movie title or owner username.
    """
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Report.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by movie_title
        movie_title = self.request.query_params.get('movie_title', None)
        if movie_title is not None:
            queryset = queryset.filter(movie__title__icontains=movie_title)

        # Filter by Owner Username
        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            queryset = queryset.filter(owner__username__icontains=owner)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReportDetailView(generics.RetrieveDestroyAPIView):
    """
    Detail of the report. Without the admin the user status only has reading
    permissions.
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
