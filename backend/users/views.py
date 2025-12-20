from rest_framework import viewsets, status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializer import UserRegisterSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing User instances.
    Provides endpoints for user registration, login, and retrieving user info.
    Arguments:
        self -- instance of the viewset
    Returns:
        Various HTTP responses based on the action performed.
    """

    queryset = User.objects.all().order_by('-id')
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Assigns permissions based on action.
        Registration and login are open to all, other actions require authentication.
        """
        if self.action in ["create", "login"]:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        """
        Personalized endpoint for user login. POST /api/users/login/
        arguments:
        request -- HttpRequest object
        returns: JWT tokens and user info if authentication is successful
        """

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email or "",
                        "first_name": user.first_name or "",
                        "last_name": user.last_name or "",
                    },
                }
            )
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)