from django.core.management.base import BaseCommand
from django.db import connection
from ics import Calendar as icsCalendar
import requests
from django.utils import timezone
from coursesCalendars.models import Course, Lesson, LessonLocation


def erase_table(table_name):
    cursor = connection.cursor()
    sql = "DELETE FROM %s;" % (table_name,)
    cursor.execute(sql)


class Command(BaseCommand):
    help = 'Drop Courses, Lessons and Lessons Location'

    def handle(self, *args, **kwargs):
        erase_table(LessonLocation._meta.db_table)
        erase_table(Lesson._meta.db_table)
        erase_table(Course._meta.db_table)

        self.stdout.write("DONE!")


