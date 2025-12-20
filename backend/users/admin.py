from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    """
    Configuration for the User model in the Django admin interface.
    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        search_fields (tuple): Fields to include in the search functionality.
        list_filter (tuple): Fields to filter the admin list view.
        ordering (tuple): Default ordering of the admin list view.
    """

    list_display = ("username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active")
    ordering = ("username",)

admin.site.register(User, UserAdmin)