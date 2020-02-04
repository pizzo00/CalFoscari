from django.db import models


class Course(models.Model):
    af_id = models.IntegerField(blank=False, null=False, verbose_name='AF ID', primary_key=True)
    name = models.CharField(blank=True, null=False, default='', verbose_name="Name", max_length=150)
    code = models.CharField(blank=False, null=False, default='CT?', verbose_name="Code", max_length=15)

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
        ]


class Calendar(models.Model):
    course = models.ForeignKey('Course', null=False, blank=False, on_delete=models.CASCADE, verbose_name="Course")
    creation_datetime = models.DateTimeField(null=False, blank=False, auto_now_add=True, verbose_name="Creation Datetime")

    def __str__(self):
        return str(self.course)

    class Meta:
        verbose_name = "Calendar"
        verbose_name_plural = "Calendars"
        indexes = [
            models.Index(fields=['creation_datetime']),
        ]


class Lesson(models.Model):
    calendar = models.ForeignKey('Calendar', null=False, blank=False, on_delete=models.CASCADE, verbose_name="Course")
    name = models.CharField(blank=False, null=False, verbose_name="Name", max_length=150)
    location = models.CharField(blank=True, null=False, default='', verbose_name="Location", max_length=150)
    begin_datetime = models.DateTimeField(null=False, blank=False, verbose_name="Begin Datetime")
    end_datetime = models.DateTimeField(null=False, blank=False, verbose_name="End Datetime")

    def __str__(self):
        return str(self.calendar) + " - " + self.name

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        indexes = [
            models.Index(fields=['begin_datetime', 'end_datetime']),
        ]