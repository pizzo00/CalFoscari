from django.core.management.base import BaseCommand
from ics import Calendar as icsCalendar
import requests
from django.utils import timezone
from univeCalendar.models import Course, Calendar, Lesson


class Command(BaseCommand):
    help = 'Save a Course Calendar in database'

    def add_arguments(self, parser):
        parser.add_argument('af_id', metavar='af_id', type=int, help='The course af id')

    def handle(self, *args, **kwargs):
        af_id = kwargs['af_id']

        url = "https://www.unive.it/data/ajax/Didattica/generaics?afid=" + str(af_id)
        ics = icsCalendar(requests.get(url).text)

        course = Course()
        course.af_id = af_id
        course.save()

        cal = Calendar()
        cal.course = course
        cal.save()

        for o in ics.events:
            l = Lesson()
            l.calendar = cal
            l.name = o.name
            l.location = o.location
            l.begin_datetime = o.begin.datetime
            l.end_datetime = o.end.datetime
            l.save()

        self.stdout.write("DONE!")
