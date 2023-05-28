from django.db import models
from users.models import User, Teacher, Student
from courses.models import Subject, Course


###TO DO Google Forms
class Event(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/')
    date = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class News(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class HomeSlide(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='home_slides/')
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class HomeSubjectSection(models.Model):
    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=300)
    description = models.TextField()
    button_text = models.CharField(max_length=100)

    def __str__(self):
        text = 'Section 1: ' + self.title
        return text

class SubjectSection1(models.Model):
    section = models.ForeignKey(HomeSubjectSection, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    position = models.IntegerField(default=0, blank=True, null=True)




class HomeCoursesSection(models.Model):
    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=300)
    description = models.TextField()
    button_text = models.CharField(max_length=100)

    def __str__(self):
        text = 'Section 2/Classes: ' + self.title
        return text

class CoursesSectionItems(models.Model):
    section = models.ForeignKey(HomeCoursesSection, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)



class HomeOurTeamSection(models.Model):
    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=300)
    description = models.TextField()
    button_text = models.CharField(max_length=100)

    def __str__(self):
        text = 'Section 3/Our Team: ' + self.title
        return text

    def get_members(self):
        return self.ourteamsectionitems_set.all()

class OurTeamSectionItems(models.Model):
    section = models.ForeignKey(HomeOurTeamSection, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    short_description = models.TextField()



class HomeAboutUsSection(models.Model):
    is_active = models.BooleanField(default=False)
    quote = models.TextField()
    title = models.CharField(max_length=300)
    description = models.TextField()
    button_text = models.CharField(max_length=100)
    image = models.ImageField(upload_to='home_about_us/')

    def __str__(self):
        text = 'Section 4/Home About Us: ' + self.title
        return text



class HomeReviewsSection(models.Model):
    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=300)

    def __str__(self):
        text = 'Section 5/Reviews: ' + self.title
        return text

class ReviewSectionItems(models.Model):
    section = models.ForeignKey(HomeReviewsSection, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    review_text = models.TextField()
    name = models.CharField(max_length=200)
    position = models.IntegerField(default=0)

class ContactUsMassage(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    massage_text = models.TextField()
    ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)