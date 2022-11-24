"""msms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from lessons import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('log_in/', views.log_in, name = 'log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('student_landing_page/', views.student_landing_page, name = 'student_landing_page'),
    path('student_lessons/', views.student_lessons, name = 'student_lessons'),
    path('student_payment/', views.student_payment, name = 'student_payment'),
    path('admin_landing_page/', views.admin_landing_page, name = 'admin_landing_page'),
    path('admin_lessons/', views.admin_lessons, name = 'admin_lessons'),
    path('admin_payment/', views.admin_payment, name = 'admin_payment'),
    path('add_children/', views.add_children, name = 'add_children'),
    path('my_children/', views.my_children, name = 'my_children'),
    path('delete_children/<childrenId>', views.delete_children, name= 'delete-children'),
    path('delete_lesson/<lessonId>', views.delete_lesson, name= 'delete-lesson'),
    path('edit_lesson/<lessonId>', views.edit_lesson, name='edit-lesson'),
    path('book_lesson/<lessonId>', views.book_lesson, name='book-lesson'),
<<<<<<< HEAD
    path('terms/', views.term_dates, name='term_dates'),
    path('view_terms/', views.view_term_dates, name='view_term_dates'),
    path('edit_terms/<term_id>', views.edit_term_dates, name='edit_term_dates'),
    path('delete_terms/<term_id>', views.delete_term_dates, name='delete_term_dates'),
=======
    path('edit_booking/<lessonId>', views.edit_booking, name='edit-booking'),
    path('delete_booking/<lessonId>', views.delete_booking, name='delete-booking')
>>>>>>> 190f2c1f9fddc1f7c8f389bc4cc5df00cad3ad4f
]
