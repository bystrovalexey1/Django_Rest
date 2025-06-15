from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "preview",
        "description",
    )
    list_filter = ("name",)
    search_fields = (
        "name",
        "description",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "preview",
        "description",
        "video_url",
        "course",
    )
    list_filter = ("course",)
    search_fields = (
        "name",
        "description",
        "course",
    )