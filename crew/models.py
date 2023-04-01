from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from movies.models import Movie


class Crew(models.Model):
    """
    Abstract base class to represent directors and actors.
    """
    crew_name = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.crew_name


class Director(Crew):
    """
    Model to represent directors, inherits from the 'Crew' model.
    """
    pass


class Actor(Crew):
    """
    Model to represent actors, inherits from the 'Crew' model.
    """
    pass


@receiver(post_save, sender=Movie)
def create_crew_for_movie(sender, instance, created, **kwargs):
    if created:
        # Loop over the directors and create Crew objects for each if they do not already exist
        for director in instance.directors.all():
            crew, created = Crew.objects.get_or_create(crew_name=director.crew_name)
            if created:
                instance.directors.add(crew)

        # Save the instance to create the movie record in the database
        instance.save()

        # Loop over the main cast and create Crew objects for each if they do not already exist
        for actor in instance.main_cast.all():
            crew, created = Crew.objects.get_or_create(crew_name=actor.crew_name)
            if created:
                instance.main_cast.add(crew)

        # Save the instance again to create the main cast Crew objects in the database
        instance.save()
