from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin
from django.contrib import admin
from .models import Student, Teacher, User, Payment, Order
from .models import User as CustomUser

class StudentInline(admin.StackedInline):
    model = Student


class StudentAdmin(admin.ModelAdmin):
    inlines = [StudentInline]


class TeacherInline(admin.StackedInline):
    model = Teacher


class TeacherAdmin(admin.ModelAdmin):
      inlines = [TeacherInline]




class StudentUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Student'



class TeacherUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Teacher'

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'is_student', 'email', 'last_login', 'phone_number')
    list_filter = ('is_student', )
    search_fields = ('username',)
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    #filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Payment)
admin.site.register(Order)
#admin.site.register(StudentUser,StudentAdmin)
#admin.site.register(TeacherUser,TeacherAdmin)
#admin.site.register(TeacherUser, ClientUserAdmin)


#admin.site.register(User, UserProfileAdmin)



#admin.site.register(Student,StudentAdmin)


# class StudentInline(admin.StackedInline):
#     model = Student
#     filter_horizontal = ('other_content',)
#
# admin.site.register(Student)
