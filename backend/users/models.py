from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    User model extending Django's AbstractUser.
    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
        email (str): The email address of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """

    def __str__(self):
        return self.username