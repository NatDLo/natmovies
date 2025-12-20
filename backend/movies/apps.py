from django.apps import AppConfig


class MoviesConfig(AppConfig):
    """
    Configuration for the 'movies' application.
    """
    
    default_auto_field = "django.db.models.BigAutoField"
    name = "movies"
