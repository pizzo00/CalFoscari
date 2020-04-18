from django.db.models import Q, Count, F
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions
from django.contrib.auth.decorators import login_required
from .serializers import CourseSerializer, UserCourseSerializer
from .models import UserCourse, Course, Lesson, LessonLocation, Color


class CoursesList(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        my_courses = self.request.query_params.get('myCourses', False)
        only_with_lesson = self.request.query_params.get('has_lesson', True)
        search = self.request.query_params.get('search', '')
        year = self.request.query_params.get('year', None)

        if my_courses:
            res = Course.objects.filter(usercourse__user=self.request.user).extra(select={'saved': 1})
        else:
            res = Course.objects.all().annotate(saved=Count('usercourse', filter=Q(usercourse__user=self.request.user)))

            if only_with_lesson:
                res = res.filter(has_lessons=True)

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


class CoursesDetail(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Course.objects.all().annotate(saved=Count('usercourse', filter=Q(usercourse__user=self.request.user)))


class UserCoursesList(generics.ListAPIView):
    serializer_class = UserCourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        qs = UserCourse.objects.filter(user=self.request.user).select_related('custom_color').annotate(custom_color_hex=F('custom_color__hex'))
        unsetted_color = qs.filter(custom_color=None)

        if unsetted_color.count() > 0:
            new_colors = Color.get_random_colors(self.request.user, len(unsetted_color))
            i = 0
            for el in unsetted_color:
                el.custom_color = new_colors[i]
                i += 1
            UserCourse.objects.bulk_update(unsetted_color, fields=['custom_color', ])
            qs = UserCourse.objects.filter(user=self.request.user).select_related('custom_color').annotate(custom_color_hex=F('custom_color__hex'))

        return qs


class UserCoursesDetail(generics.RetrieveAPIView):
    serializer_class = UserCourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return UserCourse.objects.filter(usercourse__user=self.request.user)


@login_required
def save_course(request, pk):
    saved = UserCourse()
    saved.user = request.user
    saved.course_id = pk
    saved.custom_color = Color.get_random_color(saved.user)
    saved.save()
    return HttpResponse(status=200)


@login_required
def unsave_course(request, pk):
    unsaved = UserCourse.objects.get(user=request.user, course_id=pk)
    unsaved.delete()
    return HttpResponse(status=200)
