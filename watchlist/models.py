from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie


class Watchlist(models.Model):
    """
    Watchlist model, related to 'owner', i.e. a User instance and Movie model.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, related_name='watchlist', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'movie']

    def __str__(self):
        return f'{self.owner} wants to watch {self.movie}'
