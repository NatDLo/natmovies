from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q

class Movie(models.Model):
    """
    Model representing a movie in the system.

    Attributes:
        title (str): The title of the movie.
        description (str): A brief description of the movie.
        release_date (date): The release date of the movie.
        genre (str): The genre of the movie.
        rating (float): The movie's rating between 0.0 and 5.0.
        cast (list): A list of actors in the movie.
        director (str): The director of the movie.
    """

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField()
    genre = models.CharField(max_length=50)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    cast = models.JSONField(blank=True, null=True) # List of actors
    director = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-title']
        constraints = [
            models.CheckConstraint(
                check=Q(rating__gte=0.0) & Q(rating__lte=5.0),
                name="movies_rating_between_0_and_5",
            )
        ]

    def __str__(self):
        """
        String representation of the Movie instance.
        """
        return f"{self.title} ({self.release_date.year}) - Genre: {self.genre}, Rating: {self.rating}"