from django.contrib import admin

# Register your models here.

from .models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', ]
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']


admin.site.register(Course, CourseAdmin)
