from django.db import models


# from datetime import datetime


class Course(models.Model):
    af_id = models.IntegerField(blank=False, null=False, verbose_name='AF ID', primary_key=True)
    ar_id = models.IntegerField(blank=False, null=False, verbose_name='AR ID')
    name = models.CharField(blank=True, null=False, default='', verbose_name="Name", max_length=150)
    code = models.CharField(blank=False, null=False, default='CT?', verbose_name="Code", max_length=15)
    year = models.SmallIntegerField(null=False, default=0, verbose_name="Year")
    partition = models.CharField(blank=True, null=False, default='', verbose_name="Partition", max_length=150)
    creation_datetime = models.DateTimeField(null=False, blank=False, auto_now_add=True, verbose_name="Creation Datetime")

    def __str__(self):
        if self.name != '':
            return self.code + '-' + self.name
        else:
            return self.code

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['name']),
            models.Index(fields=['ar_id']),
        ]


class Lesson(models.Model):
    ar_id = models.IntegerField(blank=False, null=False, verbose_name='AR ID')
    begin_datetime = models.DateTimeField(null=False, blank=False, verbose_name="Begin Datetime")
    end_datetime = models.DateTimeField(null=False, blank=False, verbose_name="End Datetime")

    locations = []

    # def __eq__(self, other):
    #     return isinstance(other, Lesson) and \
    #            self.ar_id == other.ar_id and \
    #            self.begin_datetime == other.begin_datetime and \
    #            self.end_datetime == other.end_datetime

    def __str__(self):
        return str(self.ar_id) + " - " + str(self.begin_datetime)

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        indexes = [
            models.Index(fields=['begin_datetime', 'end_datetime']),
        ]


class LessonLocation(models.Model):
    lesson = models.ForeignKey('Lesson', null=False, blank=False, on_delete=models.CASCADE, verbose_name="Lesson")
    location = models.CharField(blank=True, null=False, default='', verbose_name="Location", max_length=150)
    name = models.CharField(blank=False, null=False, verbose_name="Name", max_length=150)
    prof = models.CharField(blank=True, null=False, default='', verbose_name="Prof", max_length=150)
    notes = models.CharField(blank=True, null=False, default='', verbose_name="Notes", max_length=150)

    def __str__(self):
        return str(self.lesson) + " - " + self.location

    class Meta:
        verbose_name = "Lesson Location"
        verbose_name_plural = "Lessons Location"
        indexes = [
            models.Index(fields=['location', ]),
        ]
