from django.db import models
from django.contrib.auth.models import User


class UserCourse(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, verbose_name="User")
    course = models.ForeignKey('Course', null=False, blank=False, on_delete=models.DO_NOTHING, verbose_name="Course")
    custom_name = models.CharField(default='', blank=True, null=False, verbose_name="Custom Name", max_length=150)
    custom_color = models.CharField(default='', blank=True, null=False, verbose_name="Custom Color", max_length=6)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.course)

    class Meta:
        verbose_name = "UserCourse"
        verbose_name_plural = "UserCourses"
        unique_together = ('user', 'course')


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
            return self.code + ' - ' + self.name
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
    id = models.IntegerField(blank=False, null=False, primary_key=True, verbose_name='ID')
    ar_id = models.IntegerField(blank=False, null=False, verbose_name='AR ID')
    begin_datetime = models.DateTimeField(null=False, blank=False, verbose_name="Begin Datetime")
    end_datetime = models.DateTimeField(null=False, blank=False, verbose_name="End Datetime")

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
    id = models.IntegerField(blank=False, null=False, primary_key=True, verbose_name='ID')
    lesson = models.ForeignKey('Lesson', null=False, blank=False, on_delete=models.CASCADE, verbose_name="Lesson")
    location = models.CharField(blank=True, null=False, default='', verbose_name="Location", max_length=150)
    name = models.CharField(blank=False, null=False, verbose_name="Name", max_length=150)
    prof = models.CharField(blank=True, null=False, default='', verbose_name="Prof", max_length=150)
    notes = models.CharField(blank=True, null=False, default='', verbose_name="Notes", max_length=150)

    def __eq__(self, other):
        return isinstance(other, Lesson) and \
               self.lesson_id == self.lesson_id and \
               self.location == other.location and \
               self.name == other.name and \
               self.prof == other.prof and \
               self.notes == other.notes

    def get_unique_string(self):
        return str(self.lesson_id) + self.location + self.name + self.prof + self.notes

    def __hash__(self):
        # return hash((self.lesson_id, self.location, self.name, self.prof, self.notes))
        s = self.get_unique_string()
        h = hash(s)
        return h

    def __str__(self):
        return str(self.lesson) + " - " + self.location

    class Meta:
        verbose_name = "Lesson Location"
        verbose_name_plural = "Lessons Locations"
        indexes = [
            models.Index(fields=['location', ]),
        ]
