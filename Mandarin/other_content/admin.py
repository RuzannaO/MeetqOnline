from django.contrib import admin
from .models import *


# Section Slides
class HomeSlideAdmin(admin.ModelAdmin):
    model = HomeSlide
    list_display = ['position', 'title', ]


# Section1
class SubjectsInHomeInline(admin.TabularInline):
    model = SubjectSection1


class Section1Admin(admin.ModelAdmin):
    inlines = [SubjectsInHomeInline]


# Section2
class ClassesInHomeInline(admin.TabularInline):
    model = CoursesSectionItems


class ClassesHomeAdmin(admin.ModelAdmin):
    inlines = [ClassesInHomeInline]


# Section3
class OurTeamInHomeInline(admin.TabularInline):
    model = OurTeamSectionItems


class OurTeamHomeAdmin(admin.ModelAdmin):
    inlines = [OurTeamInHomeInline]


# Section5
class ReviewsInHomeInline(admin.TabularInline):
    model = ReviewSectionItems


class ReviewsHomeAdmin(admin.ModelAdmin):
    inlines = [ReviewsInHomeInline]


admin.site.register(HomeSubjectSection, Section1Admin)
admin.site.register(HomeCoursesSection, ClassesHomeAdmin)
admin.site.register(HomeOurTeamSection, OurTeamHomeAdmin)
admin.site.register(HomeReviewsSection, ReviewsHomeAdmin)
admin.site.register(HomeSlide, HomeSlideAdmin)
admin.site.register(HomeAboutUsSection)
admin.site.register(Event)
admin.site.register(News)
admin.site.register(ContactUsMassage)

