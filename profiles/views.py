from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from flixmix_rest_api.permissions import IsOwnerOrAdminOrReadOnly


class ProfileList(generics.ListAPIView):
    # Only list profiles (creation is done with signals)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    # Retrieve or update data if user is owner or admin
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
