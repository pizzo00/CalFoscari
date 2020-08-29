from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import random


class Color(models.Model):
    r = models.PositiveSmallIntegerField(blank=False, null=False, validators=[MinValueValidator(0), MaxValueValidator(255)], verbose_name='Red')
    g = models.PositiveSmallIntegerField(blank=False, null=False, validators=[MinValueValidator(0), MaxValueValidator(255)], verbose_name='Green')
    b = models.PositiveSmallIntegerField(blank=False, null=False, validators=[MinValueValidator(0), MaxValueValidator(255)], verbose_name='Blue')
    hex = models.CharField(max_length=7, blank=True, null=True, verbose_name='Hex Notation')

    def get_hex_notation(self):
        if self.r is None or self.g is None or self.b is None:
            return ''
        else:
            return '#' + format(self.r, '02x') + format(self.g, '02x') + format(self.b, '02x')

    def save(self, *args, **kwargs):
        self.hex = self.get_hex_notation()
        super().save(args, kwargs)

    def __str__(self):
        if self.hex is None:
            return ''
        else:
            return self.hex

    @staticmethod
    def get_random_color(user: User):
        used_color_id_list = UserCourse.objects.filter(user=user).values_list('custom_color', flat=True)
        all_colors = Color.objects.all()
        remaining_colors = all_colors.exclude(pk__in=used_color_id_list)

        if len(remaining_colors) == 0:
            remaining_colors = all_colors

        if len(remaining_colors) == 0:
            return None
        else:
            return random.choice(remaining_colors)

    @staticmethod
    def get_random_colors(user: User, qty: int):
        used_color_id_list = UserCourse.objects.filter(user=user).values_list('custom_color', flat=True)
        all_colors = Color.objects.all()
        remaining_colors = all_colors.exclude(pk__in=used_color_id_list)

        if len(remaining_colors) == 0:
            remaining_colors = all_colors

        if len(remaining_colors) == 0:
            return None
        else:
            if len(remaining_colors) >= qty:
                return random.choices(remaining_colors, k=qty)  # The remaining_colors is enough
            else:
                return random.choices(all_colors, k=qty)  # The remaining_colors isn't enough

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"


class UserCourse(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, verbose_name="User")
    course = models.ForeignKey('Course', null=False, blank=False, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name="Course")
    custom_name = models.CharField(default='', blank=True, null=False, verbose_name="Custom Name", max_length=250)
    custom_color = models.ForeignKey(Color, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Custom Color")

    def __str__(self):
        return str(self.user) + ' - ' + str(self.course)

    class Meta:
        verbose_name = "UserCourse"
        verbose_name_plural = "UserCourses"
        unique_together = ('user', 'course')


class Degree(models.Model):
    degree_code = models.CharField(blank=False, null=False, max_length=15, verbose_name='Degree Code')
    curriculum_code = models.CharField(blank=False, null=False, max_length=15, verbose_name='Curriculum Code')
    degree_type_code = models.CharField(blank=False, null=False, max_length=15, verbose_name='Type of Degree Code')
    degree_description = models.CharField(blank=False, null=False, max_length=250, verbose_name='Degree Description')
    curriculum_description = models.CharField(blank=False, null=False, max_length=250, verbose_name='Curriculum Description')
    degree_type_description = models.CharField(blank=False, null=False, max_length=250, verbose_name='Type of Degree Description')

    def __str__(self):
        return self.degree_code + ' - ' + self.curriculum_code

    class Meta:
        verbose_name = "Degree"
        verbose_name_plural = "Degrees"
        unique_together = ('degree_code', 'curriculum_code',)
        indexes = [
            models.Index(fields=['degree_code']),
            models.Index(fields=['degree_description']),
            models.Index(fields=['curriculum_description']),
        ]


class DegreeCourses(models.Model):
    degree_code = models.CharField(blank=False, null=False, max_length=15, verbose_name='Degree Code')
    curriculum_code = models.CharField(blank=False, null=False, max_length=15, verbose_name='Curriculum Code')
    af_id = models.IntegerField(blank=False, null=False, verbose_name='AF ID')

    def __str__(self):
        return self.degree_code + ' - ' + str(self.af_id)

    class Meta:
        verbose_name = "DegreeCourses"
        verbose_name_plural = "DegreesCourses"
        unique_together = ('degree_code', 'curriculum_code', 'af_id')
        indexes = [
            models.Index(fields=['degree_code', 'curriculum_code']),
        ]


class Course(models.Model):
    af_id = models.IntegerField(blank=False, null=False, verbose_name='AF ID', primary_key=True)
    ar_id = models.IntegerField(blank=False, null=False, verbose_name='AR ID')
    name = models.CharField(blank=True, null=False, default='', verbose_name="Name", max_length=250)
    code = models.CharField(blank=False, null=False, default='CT?', verbose_name="Code", max_length=15)
    year = models.PositiveSmallIntegerField(null=False, default=0, verbose_name="Year")
    partition = models.CharField(blank=True, null=False, default='', verbose_name="Partition", max_length=250)
    creation_datetime = models.DateTimeField(null=False, blank=False, auto_now_add=True, verbose_name="Creation Datetime")
    has_lessons = models.BooleanField(null=False, blank=False, default=True, verbose_name="Has Lesson")

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

    @staticmethod
    def get_ar_ids_of_courses_with_lessons():
        return Lesson.objects.all().values_list('ar_id', flat=True).distinct()

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
    location = models.CharField(blank=True, null=False, default='', verbose_name="Location", max_length=250)
    name = models.CharField(blank=False, null=False, verbose_name="Name", max_length=25)
    prof = models.CharField(blank=True, null=False, default='', verbose_name="Prof", max_length=150)
    notes = models.CharField(blank=True, null=False, default='', verbose_name="Notes", max_length=700)

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
