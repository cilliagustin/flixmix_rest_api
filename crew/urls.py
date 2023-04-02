from django.urls import path
from crew import views

urlpatterns = [
    path('actors/', views.ActorList.as_view()),
    path('actors/<int:pk>/', views.ActorDetailView.as_view()),
    path('directors/', views.DirectorList.as_view()),
    path('directors/<int:pk>/', views.DirectorDetailView.as_view()),
]
