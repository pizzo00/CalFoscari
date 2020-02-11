from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions
from django.contrib.auth.decorators import login_required
from .serializers import CourseSerializer
from .models import Course, Lesson, LessonLocation


class CoursesList(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        search = self.request.query_params.get('search', '')
        year = self.request.query_params.get('year', None)

        res = Course.objects.all()

        if year is not None and year.isdigit():
            res = res.filter(year__exact=year)

        if search is not '':
            if search.isdigit():
                res = res.filter(
                    Q(af_id__exact=search) |
                    Q(ar_id__exact=search) |
                    Q(name__icontains=search) |
                    Q(code__icontains=search) |
                    Q(partition__icontains=search)
                )
            else:
                res = res.filter(
                    Q(name__icontains=search) |
                    Q(code__icontains=search) |
                    Q(partition__icontains=search)
                )
        else:
            res = []

        return res


