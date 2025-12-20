from datetime import date, timedelta
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from movies.models import Movie

class MoviesAPITests(APITestCase):
    def setUp(self):
        # User and JWT login
        self.username = "tester"
        self.password = "secret123"
        get_user_model().objects.create_user(username=self.username, password=self.password)

        login_url = "/api/auth/login/"
        res = self.client.post(login_url, {"username": self.username, "password": self.password}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.content)
        self.access = res.data["access"]

        self.auth_client = APIClient()
        self.auth_client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

        self.list_url = reverse("movie-list")

    def _movie_payload(self, **overrides):
        base = {
            "title": "Interstellar",
            "description": "Space epic",
            "release_date": date(2014, 11, 7),
            "genre": "Sci-Fi",
            "rating": 8.6,
            "cast": [{"name": "Matthew McConaughey"}],
        }
        base.update(overrides)
        # Ensure date is in ISO format for JSON serialization
        if isinstance(base["release_date"], date):
            base["release_date"] = base["release_date"].isoformat()
        return base

    def test_unauthenticated_list_returns_401(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_list_empty(self):
        res = self.auth_client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)
        self.assertEqual(res.data["results"], [])

    def test_create_movie(self):
        payload = self._movie_payload()
        res = self.auth_client.post(self.list_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.content)
        self.assertTrue(Movie.objects.filter(title="Interstellar").exists())

    def test_retrieve_update_delete_movie(self):
        # Create
        create = self.auth_client.post(self.list_url, self._movie_payload(title="Inception", rating=8.8), format="json")
        self.assertEqual(create.status_code, status.HTTP_201_CREATED)
        movie_id = create.data["id"]
        detail_url = reverse("movie-detail", args=[movie_id])

        # Retrieve
        get = self.auth_client.get(detail_url)
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertEqual(get.data["title"], "Inception")

        # PATCH
        patch = self.auth_client.patch(detail_url, {"rating": 9.0}, format="json")
        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(patch.data["rating"], 9.0)

        # PUT (full update)
        put_payload = self._movie_payload(title="Inception (Final Cut)", rating=9.1)
        put = self.auth_client.put(detail_url, put_payload, format="json")
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(put.data["title"], "Inception (Final Cut)")

        # DELETE
        delete = self.auth_client.delete(detail_url)
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Movie.objects.filter(id=movie_id).exists())

    def test_filter_by_genre(self):
        for title, genre in [("A", "Drama"), ("B", "Drama"), ("C", "Comedy")]:
            self.auth_client.post(self.list_url, self._movie_payload(title=title, genre=genre), format="json")

        res = self.auth_client.get(f"{self.list_url}?genre=Drama")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 2)
        self.assertTrue(all(m["genre"] == "Drama" for m in res.data["results"]))

    def test_filter_by_rating_gte(self):
        for title, rating in [("A", 6.5), ("B", 7.5), ("C", 9.0)]:
            self.auth_client.post(self.list_url, self._movie_payload(title=title, rating=rating), format="json")

        res = self.auth_client.get(f"{self.list_url}?rating=7.5")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ratings = [m["rating"] for m in res.data["results"]]
        self.assertTrue(all(r >= 7.5 for r in ratings))

    def test_filter_with_invalid_rating_is_ignored(self):
        for title, rating in [("A", 6.5), ("B", 7.5)]:
            self.auth_client.post(self.list_url, self._movie_payload(title=title, rating=rating), format="json")

        res = self.auth_client.get(f"{self.list_url}?rating=badvalue")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 2)  # no filter applied

    def test_pagination_page_size_default(self):
        # Creates 12 movies to test pagination (default page size is 10)
        base_day = date(2020, 1, 1)
        for i in range(12):
            self.auth_client.post(
                self.list_url,
                self._movie_payload(
                    title=f"M{i:02}",
                    release_date=(base_day + timedelta(days=i)).isoformat(),
                    rating=5.0 + i * 0.1,
                ),
                format="json",
            )

        res = self.auth_client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("count", res.data)
        self.assertEqual(res.data["count"], 12)
        self.assertEqual(len(res.data["results"]), 10)