from django.db.models import Q, Count
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions
from django.contrib.auth.decorators import login_required
from .serializers import CourseSerializer
from .models import UserCourse, Course, Lesson, LessonLocation


class CoursesList(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        my_courses = self.request.query_params.get('myCourses', False)
        search = self.request.query_params.get('search', '')
        year = self.request.query_params.get('year', None)

        if my_courses:
            res = Course.objects.filter(usercourse__user=self.request.user).extra(select={'saved': 1})
        else:
            res = Course.objects.all().annotate(saved=Count('usercourse', filter=Q(usercourse__user=self.request.user)))

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


@login_required
def save_course(request, pk):
    saved = UserCourse()
    saved.user = request.user
    saved.course_id = pk
    saved.save()
    return HttpResponse(status=200)


@login_required
def unsave_course(request, pk):
    unsaved = UserCourse.objects.get(user=request.user, course_id=pk)
    unsaved.delete()
    return HttpResponse(status=200)
