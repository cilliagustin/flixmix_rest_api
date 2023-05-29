from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie


class Report(models.Model):
    """
    Report model, related to 'owner', i.e. a User instance and movie model.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'movie']

    def __str__(self):
        return f'{self.owner} reported {self.movie}'
