from django.contrib import admin
from .models import User
from .models import Lesson

# Register your models here.
admin.site.enable_nav_sidebar = False
# admin.site.site_header = 'Music Scool Director'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration fo the admin interface for users."""
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')
    fields = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')
    
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
     list_display = ('id', 'is_confirmed')