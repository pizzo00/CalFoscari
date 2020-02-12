from rest_framework import serializers
from .models import Course, Lesson, LessonLocation


class CourseSerializer(serializers.ModelSerializer):
    saved = serializers.BooleanField()

    class Meta:
        model = Course
        fields = ('af_id', 'ar_id', 'name', 'code', 'year', 'partition', 'saved')
