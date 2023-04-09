from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from profiles.models import Profile
from movies.models import Movie


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'movie']

    def __str__(self):
        return f'{self.owner} rated {self.movie}'
