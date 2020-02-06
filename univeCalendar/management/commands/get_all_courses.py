from django.core.management.base import BaseCommand
import json
import requests
from univeCalendar.models import Course, Lesson, LessonLocation
from datetime import datetime


def get_site():
    url = "https://static.unive.it/sitows/didattica/sedi"
    sites_json = json.loads(requests.get(url).text)

    output = dict()
    for s in sites_json:
        output[s['SEDE_ID']] = s['NOME']

    return output


def get_location(sites):
    url = "https://static.unive.it/sitows/didattica/aule"
    locations_json = json.loads(requests.get(url).text)

    output = dict()
    for l in locations_json:
        if l['SEDE_ID'] in sites:
            output[l['AULA_ID']] = l['NOME'] + ' - ' + sites[l['SEDE_ID']]
        else:
            output[l['AULA_ID']] = l['NOME']

    return output


def get_course():
    url = "https://static.unive.it/sitows/didattica/insegnamenti"
    courses_json = json.loads(requests.get(url).text)

    courses = []
    for c in courses_json:
        course = Course()
        course.af_id = c['AF_ID']
        course.ar_id = c['AR_ID']
        course.name = c['NOME'] if c['NOME'] else ""
        course.code = c['CODICE'] if c['CODICE'] else ""
        course.year = c['ANNO_CORSO'] if c['ANNO_CORSO'] else 0
        course.partition = c['PARTIZIONE'] if c['PARTIZIONE'] else ""
        courses.append(course)
    Course.objects.bulk_create(courses)


def get_lessons(locations):
    url = "https://static.unive.it/sitows/didattica/lezioni"
    lessons_json = json.loads(requests.get(url).text)

    lessons = []
    lessons_locations = []
    for l in lessons_json:
        ar_id = int(l['AR_ID'])
        begin_datetime = datetime.strptime(l['GIORNO'] + ' ' + l['INIZIO'], '%Y-%m-%d %H:%M')
        end_datetime = datetime.strptime(l['GIORNO'] + ' ' + l['FINE'], '%Y-%m-%d %H:%M')

        lesson = Lesson(ar_id=ar_id, begin_datetime=begin_datetime, end_datetime=end_datetime)
        if lesson not in lessons:
            lessons.append(lesson)
        else:
            lesson = next(x for x in lessons if x == lesson)

        lesson_location = LessonLocation()
        lesson_location.lesson = lesson
        lesson_location.name = l['TIPO_ATTIVITA'] if l['TIPO_ATTIVITA'] else ''
        lesson_location.location = locations[l['AULA_ID']] if l['AULA_ID'] in locations else ""
        lesson_location.prof = l['DOCENTI'] if l['DOCENTI'] else ''
        lesson_location.notes = l['NOTE'] if l['NOTE'] else ''
        lessons_locations.append(lesson_location)
    Lesson.objects.bulk_create(lessons)
    LessonLocation.objects.bulk_create(lessons_locations)


def get_lessons2(locations):
    url = "https://static.unive.it/sitows/didattica/lezioni"
    lessons_json = json.loads(requests.get(url).text)

    lessons_dict = {}
    for l in lessons_json:
        ar_id = int(l['AR_ID'])
        begin_datetime = datetime.strptime(l['GIORNO'] + ' ' + l['INIZIO'], '%Y-%m-%d %H:%M')
        end_datetime = datetime.strptime(l['GIORNO'] + ' ' + l['FINE'], '%Y-%m-%d %H:%M')

        lesson_location = LessonLocation()
        # lesson_location.lesson = lesson
        lesson_location.name = l['TIPO_ATTIVITA'] if l['TIPO_ATTIVITA'] else ''
        lesson_location.location = locations[l['AULA_ID']] if l['AULA_ID'] in locations else ''
        lesson_location.prof = l['DOCENTI'] if l['DOCENTI'] else ''
        lesson_location.notes = l['NOTE'] if l['NOTE'] else ''

        key = (ar_id, begin_datetime, end_datetime)
        if key in lessons_dict:
            lessons_dict[(ar_id, begin_datetime, end_datetime)].append(lesson_location)
        else:
            lessons_dict[(ar_id, begin_datetime, end_datetime)] = [lesson_location]

    lessons = []
    lessons_locations = {}
    pk = 0
    pk_location = 0
    for k, vs in lessons_dict.items():
        pk += 1
        lesson = Lesson(pk=pk, ar_id=k[0], begin_datetime=k[1], end_datetime=k[2])
        lessons.append(lesson)
        for lesson_location in vs:
            lesson_location.lesson_id = pk
            us = lesson_location.get_unique_string()
            if us not in lessons_locations:
                lessons_locations[us] = lesson_location
    Lesson.objects.bulk_create(lessons)
    LessonLocation.objects.bulk_create(lessons_locations.values())


class Command(BaseCommand):
    help = 'Save a all Course in database'

    def handle(self, *args, **kwargs):
        get_course()
        s = get_site()
        l = get_location(s)
        get_lessons2(l)

        self.stdout.write("DONE!")
