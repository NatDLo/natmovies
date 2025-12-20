from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

User = get_user_model()

class UsersAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse("user-list")  # /api/auth/users/
        # SimpleJWT endpoints montados bajo api/auth/
        self.jwt_login_url = "/api/auth/login/"
        self.jwt_refresh_url = "/api/auth/token/refresh/"

        # Usuario inicial
        self.username = "tester"
        self.password = "secret123"
        self.email = "tester@example.com"
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email)

        # Login para cliente autenticado
        res = self.client.post(self.jwt_login_url, {"username": self.username, "password": self.password}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.content)
        self.access = res.data["access"]
        self.auth = APIClient()
        self.auth.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

    def test_register_user_success(self):
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "StrongPass123",
        }
        res = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.content)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        # No debe devolver password
        self.assertNotIn("password", res.data)

    def test_register_user_duplicate_email(self):
        payload = {
            "username": "other",
            "email": self.email,  # duplicado
            "first_name": "Other",
            "last_name": "User",
            "password": "AnotherPass123",
        }
        res = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", res.data)

    def test_jwt_login_and_refresh(self):
        # login
        res = self.client.post(self.jwt_login_url, {"username": self.username, "password": self.password}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        access = res.data["access"]
        refresh = res.data["refresh"]
        # refresh
        res2 = self.client.post(self.jwt_refresh_url, {"refresh": refresh}, format="json")
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertIn("access", res2.data)
        # usar access para acceder a /api/auth/users/
        res3 = self.client.get(self.register_url, HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(res3.status_code, status.HTTP_200_OK)

    def test_list_requires_auth(self):
        res = self.client.get(self.register_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_list_and_retrieve_update(self):
        # listado
        res = self.auth.get(self.register_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("results", res.data)

        # crear otro usuario
        create = self.auth.post(self.register_url, {
            "username": "upduser",
            "email": "upd@example.com",
            "first_name": "Upd",
            "last_name": "User",
            "password": "UpdPass123",
        }, format="json")
        self.assertEqual(create.status_code, status.HTTP_201_CREATED, create.content)
        user_id = create.data["id"]
        detail_url = reverse("user-detail", args=[user_id])

        # retrieve
        get = self.auth.get(detail_url)
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertEqual(get.data["username"], "upduser")

        # patch
        patch = self.auth.patch(detail_url, {"first_name": "Updated"}, format="json")
        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(patch.data["first_name"], "Updated")

        # put (sin password)
        put = self.auth.put(detail_url, {
            "username": "upduser",
            "email": "upd@example.com",
            "first_name": "Full",
            "last_name": "Name",
            "password": "IgnoredPass123",  # write_only, no debe retornar
        }, format="json")
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(put.data["first_name"], "Full")
        self.assertNotIn("password", put.data)

    def test_cannot_create_without_password(self):
        res = self.client.post(self.register_url, {
            "username": "nopass",
            "email": "nopass@example.com",
            "first_name": "No",
            "last_name": "Pass",
            # sin password
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", res.data)