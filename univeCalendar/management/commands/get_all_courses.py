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

    lesson_locations = []
    for l in lessons_json:
        ar_id = int(l['AR_ID'])
        begin_datetime = datetime.strptime(l['GIORNO'] + ' ' + l['INIZIO'], '%Y-%m-%d %H:%M')
        end_datetime = datetime.strptime(l['GIORNO'] + ' ' + l['FINE'], '%Y-%m-%d %H:%M')

        lesson, created = Lesson.objects.get_or_create(ar_id=ar_id, begin_datetime=begin_datetime, end_datetime=end_datetime)

        lesson_location = LessonLocation()
        lesson_location.lesson = lesson
        lesson_location.name = l['TIPO_ATTIVITA'] if l['TIPO_ATTIVITA'] else ''
        lesson_location.location = locations[l['AULA_ID']] if l['AULA_ID'] in locations else ""
        lesson_location.prof = l['DOCENTI'] if l['DOCENTI'] else ''
        lesson_location.notes = l['NOTE'] if l['NOTE'] else ''
        lesson_locations.append(lesson_location)
    LessonLocation.objects.bulk_create(lesson_locations)


class Command(BaseCommand):
    help = 'Save a all Course in database'

    def handle(self, *args, **kwargs):
        get_course()
        s = get_site()
        l = get_location(s)
        get_lessons(l)

        self.stdout.write("DONE!")
