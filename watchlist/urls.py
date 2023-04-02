from django.urls import path
from watchlist import views

urlpatterns = [
    path('watchlist/', views.WatchlistList.as_view()),
    path('watchlist/<int:pk>/', views.WatchlistDetailView.as_view())
]
