from django.contrib import admin

from .models import *



class CoursesInSubjectInline(admin.TabularInline):
	model = Course


class TeacherCommentAdmin(admin.ModelAdmin):
    list_display = ['comment_text','create_at']

class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ['comment_text','create_at']





admin.site.register(CourseComment,CourseCommentAdmin)
admin.site.register(Course)
admin.site.register(CourseParticipant)
admin.site.register(Subject)
admin.site.register(HomeSubject)
admin.site.register(HomeCourse)
admin.site.register(ApplicantNotRegistered)
admin.site.register(ApplicationFromHome)

