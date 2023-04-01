from django.contrib import admin
from .models import Director, Actor

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    pass


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    pass