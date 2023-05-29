from django.db import models
from django.contrib.auth.models import User
from lists.models import List
from ratings.models import Rating


class CommentBase(models.Model):
    """
    Comment model, related to User and Post
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.content


class ListComment(CommentBase):
    """
    ListComment inherits from CommentBase and adds the list
    """
    list = models.ForeignKey(
        List, related_name='listcomment', on_delete=models.CASCADE
    )


class RatingComment(CommentBase):
    """
    RatingComment inherits from CommentBase and adds the rating
    """
    rating = models.ForeignKey(
        Rating, related_name='ratingcomment', on_delete=models.CASCADE
    )
