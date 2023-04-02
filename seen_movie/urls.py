from django.urls import path
from seen_movie import views

urlpatterns = [
    path('seen/', views.SeenList.as_view()),
    path('seen/<int:pk>/', views.SeenDetailView.as_view())
]
