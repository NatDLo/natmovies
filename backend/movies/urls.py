from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import MovieApiCreate

router = DefaultRouter()
router.register(r"movies", MovieApiCreate, basename="movie")

urlpatterns = router.urls