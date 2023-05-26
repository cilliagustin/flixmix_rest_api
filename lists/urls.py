from django.urls import path
from lists import views

urlpatterns = [
    path('lists/', views.ListList.as_view()),
    path('lists/<int:pk>/', views.ListDetailView.as_view())
]
