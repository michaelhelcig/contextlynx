from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


# Register your models here.

# User Admin (Custom UserAdmin)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass
