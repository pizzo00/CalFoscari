from django.db.models import Q, Count, Prefetch, F
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions
from django.contrib.auth.decorators import login_required
from .models import UserCourse, Course, Lesson, LessonLocation
import json
from datetime import datetime


@login_required
def get_calendar(request):
    from_time = request.GET.get('from', None)
    to_time = request.GET.get('to', None)

    if from_time is None or to_time is None:
        return HttpResponse(status=400)

    from_time = datetime.strptime(from_time, '%Y-%m-%d')
    to_time = datetime.strptime(to_time + ' 00:01', '%Y-%m-%d %H:%M')  # End Time Exclusive

    user_courses = UserCourse.objects.filter(user=request.user).select_related('course').select_related('custom_color')
    lessons = Lesson.objects\
        .filter(
            ar_id__in=user_courses.values_list('course__ar_id', flat=True),
            begin_datetime__gte=from_time,
            begin_datetime__lte=to_time,
        )\
        .prefetch_related('lessonlocation_set')

    data = {}
    courses_json = {}
    for c in user_courses:
        courses_json[c.course.ar_id] = {}
        # courses_json[c.course.ar_id]['af_id'] = c.course.af_id
        courses_json[c.course.ar_id]['af_id'] = c.course.af_id
        courses_json[c.course.ar_id]['name'] = c.course.name
        courses_json[c.course.ar_id]['code'] = c.course.code
        courses_json[c.course.ar_id]['partition'] = c.course.partition
        courses_json[c.course.ar_id]['custom_name'] = c.custom_name
        courses_json[c.course.ar_id]['custom_color'] = c.custom_color.hex
    data['courses'] = courses_json

    lessons_json = {}
    for l in lessons:
        lessons_json[l.id] = {
            # 'id': l.id,
            'ar_id': l.ar_id,
            'begin_datetime': l.begin_datetime.isoformat(),
            'end_datetime': l.end_datetime.isoformat(),
            'locations': []}
        for ll in l.lessonlocation_set.all():
            lessons_json[l.id]['locations'].append({
                'location': ll.location,
                'name': ll.name,
                'prof': ll.prof,
                'notes': ll.notes
            })
    data['lessons'] = lessons_json

    return HttpResponse(json.dumps(data), status=200)
