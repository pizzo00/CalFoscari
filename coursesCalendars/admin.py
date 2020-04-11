from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import UserCourse, Course, Lesson, LessonLocation, Color


class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')
    search_fields = ('id', '__str__')
    # list_filter = ('user',)
    readonly_fields = ('hex', 'color_preview', )

    def color_preview(self, instance):
        hex_notation = ''
        if instance is not None:
            hex_notation = instance.get_hex_notation()
        return format_html("<div style=\"height: 30px; width: 30px; background-color: {}\"></div>", hex_notation)


class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
    search_fields = ('user', 'course')
    list_filter = ('user', )
    readonly_fields = ('course', 'user', )


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


admin.site.register(Color, ColorAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonLocation, LessonLocationAdmin)
