from django.contrib import admin
from .models import User, Taste


@admin.register(User, Taste)
class UserAdmin(admin.ModelAdmin):
    pass
