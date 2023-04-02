from rest_framework import generics, permissions
from flixmix_rest_api.permissions import IsAdminOrReadOnly
from .models import Actor, Director
from .serializers import DirectorSerializer, ActorSerializer


class ActorList(generics.ListAPIView):
    """
    View to list all actors. they are created using signals
    """
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class DirectorList(generics.ListAPIView):
    """
    View to list all actors. they are created using signals
    """
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class ActorDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update or update data if user isadmin
    permission_classes = [IsAdminOrReadOnly]
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class DirectorDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update or update data if user isadmin
    permission_classes = [IsAdminOrReadOnly]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
