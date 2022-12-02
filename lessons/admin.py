from django.contrib import admin
from .models import User
from .models import Lesson
from .models import TermDates, Schedule

# Register your models here.
admin.site.enable_nav_sidebar = False
admin.site.site_header = 'Music School Director'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration fo the admin interface for users."""
    list_display = ('email', 'first_name', 'last_name', 'is_teacher', 'is_staff', 'is_superuser', 'is_active')
    fields = ('email', 'first_name', 'last_name','is_teacher', 'is_staff', 'is_superuser', 'is_active')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
     list_display = ('id', 'is_confirmed')


@admin.register(TermDates)
class TermAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date')

@admin.register(Schedule)
class TermAdmin(admin.ModelAdmin):
    list_display = ('start_date','interval','number_of_lessons','duration')
