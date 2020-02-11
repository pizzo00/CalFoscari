from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Course, Lesson, LessonLocation


class CourseAdmin(admin.ModelAdmin):
    list_display = ('ar_id', 'name', 'code', 'creation_datetime')
    search_fields = ('af_id', 'ar_id', 'name', 'code')
    list_filter = ('creation_datetime', )
    readonly_fields = ('lessons', )

    def lessons(self, instance):
        return format_html("<a href=\"../../../lesson/?ar_id={}\">{}</a>", str(instance.ar_id), 'Lessons')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'begin_datetime', 'end_datetime')
    search_fields = ('id', 'ar_id', 'begin_datetime', 'end_datetime')
    list_filter = ('begin_datetime', 'end_datetime')
    readonly_fields = ('locations', )

    def locations(self, instance):
        return format_html("<a href=\"../../../lessonlocation/?lesson_id={}\">{}</a>", str(instance.id), 'Locations')


class LessonLocationAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'name', 'location')
    search_fields = ('id', 'lesson_id', 'location', 'name', 'prof', 'notes')
    readonly_fields = ('lesson', )


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonLocation, LessonLocationAdmin)
