from django.core.management.base import BaseCommand
import json
import requests
from coursesCalendars.models import Course, Lesson, LessonLocation, Degree, DegreeCourses
from datetime import datetime


def get_degrees():
    url = "http://apps.unive.it/sitows/didattica/corsi"
    degrees_json = json.loads(requests.get(url).text)

    degrees = []
    for d in degrees_json:
        degree = Degree()
        degree.degree_code = d['CDS_COD']
        degree.curriculum_code = d['PDS_COD']
        degree.degree_type_code = d['TIPO_CORSO_COD']
        degree.degree_description = d['CDS_DES']
        degree.curriculum_description = d['PDS_DES']
        degree.degree_type_description = d['TIPO_CORSO_DES']
        degrees.append(degree)
    Degree.objects.bulk_create(degrees)


def get_degrees_courses():
    url = "https://apps.unive.it/sitows/didattica/corsiinsegnamenti"
    degrees_courses_json = json.loads(requests.get(url).text)

    degrees_courses = []
    for dc in degrees_courses_json:
        degree_courses = DegreeCourses()
        degree_courses.degree_code = dc['CDS_COD']
        degree_courses.curriculum_code = dc['PDS_COD']
        degree_courses.af_id = dc['AF_ID']
        degrees_courses.append(degree_courses)
    DegreeCourses.objects.bulk_create(degrees_courses)


def get_sites():
    url = "https://apps.unive.it/sitows/didattica/sedi"
    sites_json = json.loads(requests.get(url).text)

    output = dict()
    for s in sites_json:
        output[s['SEDE_ID']] = s['NOME']

    return output


def get_locations(sites):
    url = "https://apps.unive.it/sitows/didattica/aule"
    locations_json = json.loads(requests.get(url).text)

    output = dict()
    for l in locations_json:
        if l['SEDE_ID'] in sites:
            output[l['AULA_ID']] = l['NOME'] + ' - ' + sites[l['SEDE_ID']]
        else:
            output[l['AULA_ID']] = l['NOME']

    return output


def get_lessons(locations):
    url = "https://apps.unive.it/sitows/didattica/lezioni"
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
        lesson = Lesson(id=pk, ar_id=k[0], begin_datetime=k[1], end_datetime=k[2])
        lessons.append(lesson)
        for lesson_location in vs:
            pk_location += 1
            lesson_location.id = pk_location
            lesson_location.lesson_id = pk
            us = lesson_location.get_unique_string()
            if us not in lessons_locations:
                lessons_locations[us] = lesson_location
    Lesson.objects.bulk_create(lessons)
    LessonLocation.objects.bulk_create(lessons_locations.values())


def get_courses(ar_ids_of_courses_with_lessons):
    url = "https://apps.unive.it/sitows/didattica/insegnamenti"
    courses_json = json.loads(requests.get(url).text)

    courses = []
    for c in courses_json:
        course = Course()
        course.af_id = c['AF_ID']
        course.ar_id = c['AR_ID']
        course.name = c['NOME'] if c['NOME'] else ""
        course.name = course.name[0].upper() + course.name[1:].lower()
        course.code = c['CODICE'] if c['CODICE'] else ""
        course.year = c['ANNO_CORSO'] if c['ANNO_CORSO'] else 0
        course.partition = c['PARTIZIONE'] if c['PARTIZIONE'] else ""
        course.has_lessons = int(course.ar_id) in ar_ids_of_courses_with_lessons
        courses.append(course)
    Course.objects.bulk_create(courses)


class Command(BaseCommand):
    help = 'Save a all Course in database'

    def handle(self, *args, **kwargs):
        get_degrees()
        get_degrees_courses()
        sites = get_sites()
        locations = get_locations(sites)
        get_lessons(locations)
        get_courses(set(Lesson.get_ar_ids_of_courses_with_lessons()))

        self.stdout.write("DONE!")
