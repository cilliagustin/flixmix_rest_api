from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=60, blank=True)
    description = models.TextField(blank=True, max_length=250)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_i0yy2i'
    )
    is_admin = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(owner=instance)
        if instance.is_superuser:
            profile.is_admin = True
            profile.save()


post_save.connect(create_profile, sender=User)
