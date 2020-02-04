from django.contrib import admin
from .models import Course, Calendar, Lesson


class CourseAdmin(admin.ModelAdmin):
    list_display = ('af_id', 'name', 'code')
    search_fields = ('af_id', 'name', 'code')
    # list_filter =
    # readonly_fields =


class CalendarAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'creation_datetime')
    search_fields = ('__str__',)
    list_filter = ('creation_datetime', )
    # readonly_fields =


class LessonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'begin_datetime', 'end_datetime')
    search_fields = ('calendar', 'name')
    list_filter = ('begin_datetime', 'end_datetime')


admin.site.register(Course, CourseAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Lesson, LessonAdmin)
