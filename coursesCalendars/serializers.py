from rest_framework import serializers
from .models import UserCourse, Course, Lesson, LessonLocation


class CourseSerializer(serializers.ModelSerializer):
    saved = serializers.BooleanField()

    class Meta:
        model = Course
        fields = ('af_id', 'ar_id', 'name', 'code', 'year', 'partition', 'saved')


class UserCourseSerializer(serializers.ModelSerializer):
    custom_color_hex = serializers.CharField()

    class Meta:
        model = UserCourse
        fields = ('course', 'custom_name', 'custom_color', 'custom_color_hex')
