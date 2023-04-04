from django.urls import path
from comments import views

urlpatterns = [
    path('listcomments/', views.ListCommentList.as_view()),
    path('listcomments/<int:pk>/', views.ListCommentDetailView.as_view()),
    path('ratingcomments/', views.RatingCommentList.as_view()),
    path('ratingcomments/<int:pk>/', views.RatingCommentDetailView.as_view())
]
