from django.urls import path

from . import views
from .views import (
    SubjectDetailView,
    CourseDetailView,
    CoursesListView,
    TutorsListView,
    TutorDetailView,
    StudentDetailView,
    CoursesListViewFilter
)

urlpatterns = [
    path('', views.home, name='home'),
    path('subject/<int:pk>/', CoursesListViewFilter.as_view(), name='subject_detail'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/', CoursesListView.as_view(), name='courses_list'),
    path('courses/subject_<int:pk>/', CoursesListViewFilter.as_view(), name='courses_list_filter'),
    path('tutors/', TutorsListView.as_view(), name='tutors_list'),
    path('teacher/<int:pk>/', TutorDetailView.as_view(), name='teacher_detail'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('addCommentToTeacher/<int:pk>/', views.addCommentToTeacher, name='addCommentToTeacher'),
    path('addCommentToCourse/<int:pk>/', views.addCommentToCourse, name='addCommentToCourse'),
    path('applyForCourseNotRegistered/<int:pk>/', views.applyForCourseNotRegistered, name='applyForCourseNotRegistered'),
    path('applicationFromHome/', views.applyFromHome, name='applyFromHome'),
    path('applyForCourse/<int:pk>/', views.applyForCourse, name='applyForCourse'),
    path('unenrollFromCourse/<int:pk>/', views.unenrollFromCourse, name='unenrollFromCourse')
]