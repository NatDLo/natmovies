from .models import Movie
from .serializer import MovieSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from django.db.models import Q

class MovieApiCreate(viewsets.ModelViewSet):
    """
    API endpoint to create, delete, and list movies.
    Allows filtering movies by genre and rating.
    arguments:
    self -- instance of the view
    returns: queryset of movies
    """

    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Gets the queryset for the Movie model
        based on the provided query parameters.
        arguments:
        self -- instance of the view
        returns: filtered queryset
        """

        query = Q()  # Start with an empty query

        param_genre = self.request.query_params.get("genre", None)
        if param_genre is not None:
            query &= Q(genre=param_genre)

        param_rating = self.request.query_params.get("rating", None)
        if param_rating is not None:
            try:
                rating = float(param_rating)
                query &= Q(rating__gte=rating)
            except ValueError:
                pass  # Ignore invalid rating filter

        # Ensure global alphabetical ordering across pagination
        queryset = Movie.objects.all().filter(query).order_by('title')
        return queryset

