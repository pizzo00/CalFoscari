from django.urls import path
from . import views

app_name = 'coursesCalendars'

urlpatterns = [
    path('courses/', views.CoursesList.as_view(), name='courses'),
    path('courses/<int:pk>/save', views.save_course, name='courses_save'),
    path('courses/<int:pk>/unsave', views.unsave_course, name='courses_unsave'),
]
