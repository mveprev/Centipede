from django.contrib import admin
from .models import Student

# Register your models here.
@admin.register(Student)
class UserAdmin(admin.ModelAdmin):
    """Configuration fo the admin interface for users."""
    list_display = [
        'email', 'first_name', 'last_name', 'is_active',
    ]
