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
]
