from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calendar', views.calendar, name='calendar'),
    path('my_courses', views.my_courses, name='my_courses'),
    path('search_courses', views.search_courses, name='search_courses'),
]
