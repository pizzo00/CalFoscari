from django.urls import path
from . import views

app_name = 'coursesCalendars'

urlpatterns = [
    path('courses/', views.CoursesList.as_view(), name='courses'),
]
