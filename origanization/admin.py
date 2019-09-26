from django.contrib import admin

# Register your models here.


from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    model_icon = 'fa fa-university'


class CourseOrgAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'click_num', 'fav_num']
    search_fields = ['name', 'desc', 'click_num', 'fav_num']
    list_filter = ['name', 'desc', 'click_num', 'fav_num']
    relfield_style = 'fk-ajax'
    style_fields = {"desc": "ueditor"}
    model_icon = 'fa fa-university'


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['org', 'name', 'work_years', 'work_company']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company']
    model_icon = 'fa fa-user-md'


admin.site.register(CityDict, CityDictAdmin)
admin.site.register(CourseOrg, CourseOrgAdmin)
admin.site.register(Teacher, TeacherAdmin)
