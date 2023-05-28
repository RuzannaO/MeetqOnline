from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image, ImageOps
import courses
from django.db.models import Avg
import datetime


class User(AbstractUser):
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=50, null=True, blank=True)



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(null=True, blank=True, max_length=300)
    image = models.ImageField(upload_to='student_images/', default='avatar.gif')
    mandarins = models.IntegerField(null=True, default=0)
    description = models.TextField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Student, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img = ImageOps.exif_transpose(img)
            img.save(self.image.path)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='teachers_images/', default='avatar.gif')
    mandarins = models.IntegerField(null=True, default=0)
    verified = models.BooleanField(default=False)
    languages = models.TextField(null=True, blank=True)
    video_link = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        full_name = 'Teacher - ' + self.user.username
        return full_name

    @property
    def avg_rate(self):
        return courses.models.TeacherComment.objects.filter(teacher=self).aggregate(Avg('rate'))['rate__avg']

    @property
    def amount_of_comments(self):
        return courses.models.TeacherComment.objects.filter(teacher=self).count()

    def save(self, *args, **kwargs):
        current_video_link = self.video_link
        video_id = current_video_link
        if current_video_link:
            if "embed" in current_video_link:
                video_id = current_video_link.split('embed/')[1].split(" ")[0][:-1]
            elif "v=" in current_video_link:
                video_id = current_video_link.split('v=')[1].split('&')[0]
        self.video_link = video_id
        super(Teacher, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img  = ImageOps.exif_transpose(img)
            img.save(self.image.path)


def year_choices():
    return [(r,r) for r in range(2021, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year

def deadline_day():
    return datetime.date.today() + datetime.timedelta(days=20)


class Payment(models.Model):
    JAN = "January"
    FEB = "February"
    MAR = "March"
    APR = "April"
    MAY = "May"
    JUN = "June"
    JUL = "Jule"
    AUG = "August"
    SEP = "September"
    OCT = "October"
    NOV = "November"
    DEC = "December"

    MONTH_CHOICES = (
        (JAN, "January"),
        (FEB, "February"),
        (MAR, "March"),
        (APR, "APRIL"),
        (MAY, "MAY"),
        (JUN, "JUNE"),
        (JUL, "JULE"),
        (AUG, "August"),
        (SEP, "September"),
        (OCT, "October"),
        (NOV, "November"),
        (DEC, "December")
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True, default=0)
    month = models.CharField(max_length=9, choices=MONTH_CHOICES,default="January")
    year = models.IntegerField(max_length=4, choices=year_choices(), default=current_year())
    is_deadline = models.BooleanField(default=True)
    deadline = models.DateField(default=deadline_day())
    is_paid = models.BooleanField(default=False)
    amount_of_lessons = models.IntegerField(max_length=4, default=1)
    canceled_lessons = models.IntegerField(max_length=4, default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.year:
            text_to_be_returned = self.student.user.username + ' - ' + self.month + ' of ' + str(self.year)
        else:
            text_to_be_returned = 'empty'
        return text_to_be_returned


class Order(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    itf_order_id = models.IntegerField(null=True, blank=True)
    last_massage = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.payment.id:
          text_to_be_returned = self.payment.student.user.username + ' - ' + str(self.payment.id)
        else:
            text_to_be_returned = "Empty"
        return text_to_be_returned