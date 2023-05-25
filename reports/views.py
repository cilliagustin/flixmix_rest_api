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
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['is_closed', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Order by is_closed (false first) and then by created_at
        queryset = queryset.order_by('is_closed', '-created_at')

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
