from rest_framework import serializers
from .models import Course, Lesson, LessonLocation


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
