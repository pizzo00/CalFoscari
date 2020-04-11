from django.core.management.base import BaseCommand
from django.db import connection
from ics import Calendar as icsCalendar
import requests
from django.utils import timezone
from coursesCalendars.models import Color


def erase_table(table_name):
    cursor = connection.cursor()
    sql = "DELETE FROM %s;" % (table_name,)
    cursor.execute(sql)


def add_color(r, g, b):
    new_color = Color()
    new_color.r = r
    new_color.g = g
    new_color.b = b
    new_color.save()


class Command(BaseCommand):
    help = 'Overwrite colors with default set'

    def handle(self, *args, **kwargs):
        erase_table(Color._meta.db_table)
        add_color(  0, 100,   0)  # #006400
        add_color(  0,   0, 139)  # #00008b
        add_color(112,  55,  55)  # #703737
        add_color(255,   0,   0)  # #ff0000
        add_color(255, 255,   0)  # #ffff00
        add_color(222, 184, 135)  # #deb887
        add_color(  0, 255,   0)  # #00ff00
        add_color(  0, 255, 255)  # #00ffff
        add_color(255,   0, 255)  # #ff00ff
        add_color(100, 149, 237)  # #6495ed

        self.stdout.write("DONE!")


