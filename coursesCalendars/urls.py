from django.urls import path
from . import views_courses, views_calendars

app_name = 'coursesCalendars'

urlpatterns = [
    path('courses/', views_courses.CoursesList.as_view(), name='courses'),
    path('courses/<int:pk>', views_courses.CoursesDetail.as_view(), name='courses_detail'),
    path('userCourses/', views_courses.UserCoursesList.as_view(), name='userCourses'),
    path('userCourses/<int:pk>', views_courses.UserCoursesDetail.as_view(), name='userCourses_detail'),
    path('courses/<int:pk>/save', views_courses.save_course, name='courses_save'),
    path('courses/<int:pk>/unsave', views_courses.unsave_course, name='courses_unsave'),
    path('calendars/', views_calendars.get_calendar, name='calendars'),
]
