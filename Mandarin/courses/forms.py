
from django import forms
from .models import TeacherComment, CourseComment, ApplicantNotRegistered, ApplicationFromHome




class CommentForm(forms.ModelForm):
    class Meta:
        model = TeacherComment
        fields = ['comment_text', 'rate']

class CourseCommentForm(forms.ModelForm):
    class Meta:
        model = CourseComment
        fields = ['comment_text', 'rate']

class TeacherCommentForm(forms.ModelForm):
    class Meta:
        model = TeacherComment
        fields = ['comment_text', 'rate']

class ApplyForCourseForm(forms.ModelForm):
    class Meta:
        model = ApplicantNotRegistered
        fields = ['full_name', 'email', 'phone_number']

class ApplyFromHomeForm(forms.ModelForm):
    class Meta:
        model = ApplicationFromHome
        fields = ['full_name', 'email', 'phone_number', 'info_text']