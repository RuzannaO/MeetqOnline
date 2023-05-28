
from django import forms
from .models import User, Student, Teacher
from django.contrib.auth.forms import UserCreationForm


class StudentRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'phone_number', 'password1', 'password2']
        help_texts = {
            'username': None
        }

    def __init__(self, *args, **kwargs):
        super(StudentRegisterForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = True

    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.is_teacher = False
        user.save()
        return user


class TeacherRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

        help_texts = {
            'username': None
        }

    def __init__(self, *args, **kwargs):
        super(TeacherRegisterForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = True

    def save(self):
        user = super().save(commit=False)
        user.is_student = False
        user.is_teacher = True
        user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CheckboxInput()


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']
        help_texts = {
            'username': None
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = True




class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['bio','description','image']
        widgets = {
            'bio': forms.TextInput(attrs={'placeholder': 'Short about yourself'}),
            'description': forms.Textarea(attrs={'placeholder': 'Please describe yourself'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['bio'].required = False
        self.fields['description'].required = False

class TeacherUpdateForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = ['bio','description','video_link','languages','image']
        widgets = {
            'bio': forms.TextInput(attrs={'placeholder': 'Short about yourself'}),
            'description': forms.Textarea(attrs={'placeholder': 'Please describe yourself'}),
            'languages': forms.TextInput(attrs={'placeholder': 'e.g. Armenian, English, Russian'}),
        }

    def __init__(self, *args, **kwargs):
        super(TeacherUpdateForm, self).__init__(*args, **kwargs)
        self.fields['bio'].required = False
        self.fields['description'].required = False
        self.fields['video_link'].required = False