from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from utils.choices import GENRES_CHOICES
from datetime import date


class Movie(models.Model):
    """
    Movie model, related to 'owner', i.e. a User instance.
    Default image set so that we can always reference image.url.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    synopsis = models.TextField(max_length=400)
    directors = models.ManyToManyField(
        'crew.Director',
        related_name='movie_director',
    )
    main_cast = models.ManyToManyField(
        'crew.Actor',
        related_name='movie_cast',
    )
    image = models.ImageField(
        upload_to='images/', default='../blank_movie_rlo48q', blank=True
    )
    release_year = models.IntegerField(
        validators=[MinValueValidator(1888), MaxValueValidator(date.today().year)]
    )
    movie_genre = models.CharField(
        max_length=20,
        choices=GENRES_CHOICES,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def avg_rating(self):
        # Import here to avoid circular import
        from ratings.models import Rating
        ratings = Rating.objects.filter(movie=self)
        if ratings.exists():
            return "{:.2f}".format(
                round(ratings.aggregate(Avg('value'))['value__avg'], 2))
        return None


    @property
    def decade(self):
        return int(self.release_year / 10) * 10

    def __str__(self):
        return self.title
