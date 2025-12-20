from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.apps import apps
from datetime import datetime

class Command(BaseCommand):
    help = "Seed superuser and 15 movies."

    def handle(self, *args, **options):
        self._ensure_superuser()
        self._seed_movies()

    def _ensure_superuser(self):
        User = get_user_model()
        obj, created = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True}
        )
        if created:
            obj.set_password("admin123")
            obj.save()
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created."))
        else:
            self.stdout.write("Superuser 'admin' already exists.")

    def _seed_movies(self):
        Movie = apps.get_model("movies", "Movie")
        fields = {f.name for f in Movie._meta.get_fields()}
        if "title" not in fields:
            self.stdout.write(self.style.ERROR("Movie model missing 'title'."))
            return

        movies = [
            {"title": "The Shawshank Redemption", "genre": "Drama", "release_date": "1994-09-23", "rating": 9.3, "director": "Frank Darabont", "description": "Hope can set you free."},
            {"title": "The Godfather", "genre": "Crime", "release_date": "1972-03-24", "rating": 9.2, "director": "Francis Ford Coppola", "description": "An offer you can't refuse."},
            {"title": "The Dark Knight", "genre": "Action", "release_date": "2008-07-18", "rating": 9.0, "director": "Christopher Nolan", "description": "Why so serious?"},
            {"title": "Pulp Fiction", "genre": "Crime", "release_date": "1994-10-14", "rating": 8.9, "director": "Quentin Tarantino", "description": "Chronologically out of order."},
            {"title": "Forrest Gump", "genre": "Drama", "release_date": "1994-07-06", "rating": 8.8, "director": "Robert Zemeckis", "description": "Life is like a box of chocolates."},
            {"title": "Inception", "genre": "Sci-Fi", "release_date": "2010-07-16", "rating": 8.8, "director": "Christopher Nolan", "description": "A dream within a dream."},
            {"title": "Fight Club", "genre": "Drama", "release_date": "1999-10-15", "rating": 8.8, "director": "David Fincher", "description": "The first rule..."},
            {"title": "The Matrix", "genre": "Sci-Fi", "release_date": "1999-03-31", "rating": 8.7, "director": "The Wachowskis", "description": "Red pill or blue pill."},
            {"title": "Goodfellas", "genre": "Crime", "release_date": "1990-09-19", "rating": 8.7, "director": "Martin Scorsese", "description": "As far back as I can remember..."},
            {"title": "Se7en", "genre": "Thriller", "release_date": "1995-09-22", "rating": 8.6, "director": "David Fincher", "description": "Seven deadly sins."},
            {"title": "Interstellar", "genre": "Sci-Fi", "release_date": "2014-11-07", "rating": 8.6, "director": "Christopher Nolan", "description": "Love transcends dimensions."},
            {"title": "The Silence of the Lambs", "genre": "Thriller", "release_date": "1991-02-14", "rating": 8.6, "director": "Jonathan Demme", "description": "Hello, Clarice."},
            {"title": "The Green Mile", "genre": "Drama", "release_date": "1999-12-10", "rating": 8.6, "director": "Frank Darabont", "description": "Miracles on death row."},
            {"title": "Gladiator", "genre": "Action", "release_date": "2000-05-05", "rating": 8.5, "director": "Ridley Scott", "description": "Are you not entertained?"},
            {"title": "City of God", "genre": "Crime", "release_date": "2002-08-30", "rating": 8.6, "director": "Fernando Meirelles", "description": "The rise of crime in Rio."},
        ]

        def to_date(s):
            try:
                return datetime.strptime(s, "%Y-%m-%d").date()
            except Exception:
                return None

        def to_rating_0_5(r):
            # convierte ratings en escala 0–10 a 0–5 y respeta el constraint
            try:
                val = float(r) / 2.0
                return max(0.0, min(5.0, val))
            except Exception:
                return None

        created, updated = 0, 0
        for m in movies:
            defaults = {}
            for k, v in m.items():
                field = k
                if field not in fields:
                    continue
                if field == "release_date":
                    defaults[field] = to_date(v)
                elif field == "rating":
                    defaults[field] = to_rating_0_5(v)
                else:
                    defaults[field] = v

            _, was_created = Movie.objects.update_or_create(
                defaults=defaults,
                **{"title": m["title"]}
            )
            created += 1 if was_created else 0
            updated += 0 if was_created else 1

        self.stdout.write(self.style.SUCCESS(f"Seed done. Created: {created}, updated: {updated}"))