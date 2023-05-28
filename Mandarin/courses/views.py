from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import *
from other_content.models import HomeSlide, HomeOurTeamSection, HomeReviewsSection
from .forms import CourseCommentForm, ApplyForCourseForm, TeacherCommentForm, ApplyFromHomeForm
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView
)



def home(request):
    home_courses = HomeCourse.objects.all().order_by('position')
    home_subjects = HomeSubject.objects.all().order_by('position')
    home_slides = HomeSlide.objects.all().order_by('position')
    slides = HomeSlide.objects.filter(position__gt=0)
    our_team = HomeOurTeamSection.objects.get(is_active=True)
    home_reviews_section = HomeReviewsSection.objects.get(is_active=True)
    result = {'home_courses': home_courses,
              'home_subjects': home_subjects,
              'home_slides': home_slides,
              'slides': slides,
              'our_team': our_team,
              'home_reviews_section': home_reviews_section
              }

    return render(request, 'home.html', result)


class SubjectDetailView(DetailView):
    model = Subject
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        context = super(SubjectDetailView, self).get_context_data(**kwargs)
        context['subject'] = self.object
        context['courses'] = Course.objects.filter(subject=self.object)
        return context

class CourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        import random
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['course'] = self.object

        all_courses = Course.objects.all()
        number_of_courses = len(all_courses)
        random_indexes = random.sample(range(0, number_of_courses), 4)
        suggested_courses = []
        for index in random_indexes:
            suggested_courses.append(all_courses[index])
        context['suggested_courses'] = suggested_courses
        #fields = Teacher._meta.get_fields()
        comments = CourseComment.objects.filter(course=self.object)
        context['comments'] = comments
        return context

class CoursesListView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'courses/courses_list.html'
    paginate_by = 12
    query_text = ''

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        if query is None:
            courses = Course.objects.all()
        else:
            self.query_text = query
            courses = Course.objects.filter(Q(name__contains=query) | Q(subject__name__contains=query))
        return courses

    def get_context_data(self, **kwargs):
        context = super(CoursesListView, self).get_context_data(**kwargs)
        subjects = Subject.objects.all()
        context['subjects'] = subjects
        context['subjects_amount'] = len(subjects)
        context['query_text'] = self.query_text

        return context


class CoursesListViewFilter(CoursesListView):

    def get_queryset(self):
        courses = super().get_queryset()
        subject_id = self.kwargs['pk']
        courses_filtered = Course.objects.filter(subject__id=subject_id)
        if len(courses_filtered) > 0:
            courses = courses_filtered
        return courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sub_id = self.kwargs['pk']
        context['subjects'] = Subject.objects.get(id=sub_id)
        context['subjects_amount'] = 1
        return context


class TutorsListView(ListView):
    model = Teacher
    context_object_name = 'teachers'
    template_name = 'teachers/teachers_list.html'
    paginate_by = 10

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        if query is None:
            tutors = Teacher.objects.filter(verified=True).order_by('-id')
        else:
            tutors = Teacher.objects.filter((Q(user__first_name__startswith=query) | Q(user__last_name__startswith=query)),verified=True)

        return tutors

    def get_context_data(self, **kwargs):
        context = super(TutorsListView, self).get_context_data(**kwargs)
        teachers = context['teachers']
        teachers_subject_dict = dict()
        for teacher in teachers:
            teacher_subjects = set()
            courses_teacher = Course.objects.filter(teacher=teacher)
            for course in courses_teacher:
                teacher_subjects.add(course.subject)
            teachers_subject_dict[teacher.user.id] = teacher_subjects

        context['teacher_subjects'] = teachers_subject_dict


        return context


class TutorDetailView(DetailView):
    model = Teacher
    context_object_name = 'teacher'
    template_name = 'teachers/teacher_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TutorDetailView, self).get_context_data(**kwargs)
        context['teacher'] = self.object
        comments = TeacherComment.objects.filter(teacher=self.object)
        context['comments'] = comments
        return context

class StudentDetailView(DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'students/student_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context['student'] = self.object
        return context


def addCommentToCourse(request,pk):
    url = request.META.get('HTTP_REFERER')
    if request.method =='POST':
        form = CourseCommentForm(request.POST)
        if form.is_valid():
            data = CourseComment()
            course = Course.objects.get(id=pk)
            data.course = course
            data.comment_text = form.cleaned_data['comment_text']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            cur_student = Student.objects.get(user=request.user)
            data.writer = cur_student
            data.save()
            messages.success(request,"Your review has been sent")
            return HttpResponseRedirect(url)

    return render(request,'home')

def addCommentToTeacher(request,pk):
    url = request.META.get('HTTP_REFERER')
    if request.method =='POST':
        form = TeacherCommentForm(request.POST)
        if form.is_valid():
            data = TeacherComment()
            teacher = Teacher.objects.get(id=pk)
            data.teacher = teacher
            data.comment_text = form.cleaned_data['comment_text']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            cur_student = Student.objects.get(user=request.user)
            data.writer = cur_student
            data.save()
            messages.success(request,"Your review has been sent")
            return HttpResponseRedirect(url)

    return render(request,'home')


def applyForCourseNotRegistered(request,pk):
    if request.method =='POST':
        form = ApplyForCourseForm(request.POST)
        if form.is_valid():
            data = ApplicantNotRegistered()
            course = Course.objects.get(id=pk)
            data.course = course
            data.full_name = form.cleaned_data['full_name']
            data.email = form.cleaned_data['email']
            data.phone_number = form.cleaned_data['phone_number']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,"Your application has been sent! We will get touch with you!")
            return HttpResponseRedirect('/signup/student')

    return render(request,'home')

def applyFromHome(request):
    if request.method =='POST':
        form = ApplyFromHomeForm(request.POST)
        if form.is_valid():
            data = ApplicationFromHome()
            data.full_name = form.cleaned_data['full_name']
            data.email = form.cleaned_data['email']
            data.phone_number = form.cleaned_data['phone_number']
            data.info_text = form.cleaned_data['info_text']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,"Your application has been sent! We will get touch with you!")
            return HttpResponseRedirect('/courses')

    return render(request,'home')


def applyForCourse(request,pk):
    data = CourseParticipant()
    course = Course.objects.get(id=pk)
    data.course = course
    data.student = Student.objects.get(user=request.user)
    data.ip = request.META.get('REMOTE_ADDR')
    data.save()
    messages.success(request, "Your application has been sent! We will get touch with you!")
    return HttpResponseRedirect('/profile/')


def unenrollFromCourse(request, pk):
    course = Course.objects.get(id=pk)
    student = Student.objects.get(user=request.user)
    CourseParticipant.objects.get(course=course,student=student).delete()
    messages.success(request, "Your have been unenrolled from the course!")
    return HttpResponseRedirect('/profile')














