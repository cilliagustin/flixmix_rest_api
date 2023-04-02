from django.contrib import admin
from .models import Movie


class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'owner', 'release_year', 'movie_genre', 'avg_rating',
        'release_decade', 'seen_count', 'watchlist_count'
    )


admin.site.register(Movie, MovieAdmin)
