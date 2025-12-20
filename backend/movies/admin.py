from django.contrib import admin
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    """
    Configuration for the Movie model in the Django admin interface.
    Allows admin users to view, search, and filter movies effectively.
    """

    list_display = ("title", "genre", "rating", "release_date")
    search_fields = ("title", "genre", "cast")
    list_filter = ("genre", "release_date", "rating")
    ordering = ("-title",)

admin.site.register(Movie, MovieAdmin)