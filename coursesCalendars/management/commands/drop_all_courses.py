from django.core.management.base import BaseCommand
from django.db import connection
from coursesCalendars.models import Course, Lesson, LessonLocation, DegreeCourses, Degree


def erase_table(table_name):
    cursor = connection.cursor()
    sql = "DELETE FROM \"%s\";" % (table_name,)
    cursor.execute(sql)


class Command(BaseCommand):
    help = 'Drop Courses, Lessons and Lessons Location'

    def handle(self, *args, **kwargs):
        erase_table(Degree._meta.db_table)
        erase_table(DegreeCourses._meta.db_table)
        erase_table(LessonLocation._meta.db_table)
        erase_table(Lesson._meta.db_table)
        erase_table(Course._meta.db_table)

        self.stdout.write("DONE!")


