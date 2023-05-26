from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie


class List(models.Model):
    """
    Model representing a user-created list of movies.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=400, blank=True)
    movies = models.ManyToManyField(Movie, related_name='lists')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
