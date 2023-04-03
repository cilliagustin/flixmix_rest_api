from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('profiles.urls')),
    path('', include('movies.urls')),
    path('', include('ratings.urls')),
    path('', include('seen_movie.urls')),
    path('', include('watchlist.urls')),
    path('', include('followers.urls')),
    path('', include('lists.urls')),
]
