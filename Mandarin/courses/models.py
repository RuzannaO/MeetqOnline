from django.db import models
from users.models import Student,Teacher
from django.db.models import Avg, Count
from PIL import Image


class Subject(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='subjects/')

    def __str__(self):
        return self.name

class HomeSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    position = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return str(self.position)


class Course(models.Model):
    name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    short_description = models.TextField(max_length=500)
    long_description = models.TextField(null=True, blank=True)
    individual = "Individual"
    group = "Group"
    both = "Individual/Group"
    ROOM_TYPES = (
        (individual, "Individual"),
        (group, "Group"),
        (both, "Individual/Group"),
    )
    room_type = models.CharField(max_length=25,
                             choices=ROOM_TYPES,
                             default="Individual")

    capacity = models.IntegerField(default=1)
    topics = models.TextField()
    video_link = models.CharField(max_length=300, null=True, blank=True)
    price_individual = models.FloatField(null=True, blank=True, default=15)
    price_group = models.FloatField(null=True, blank=True, default=10)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='courses/')
    min_age_individual = models.IntegerField(null=True, blank=True)
    max_age_individual = models.IntegerField(null=True, blank=True)
    min_age_group = models.IntegerField(null=True, blank=True)
    max_age_group = models.IntegerField(null=True, blank=True)
    duration_individual = models.CharField(null=True, blank=True, max_length=300)
    duration_group = models.CharField(null=True, blank=True, max_length=300)
    class_per_week_individual = models.IntegerField(null=True, blank=True, default=1)
    class_per_week_group = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return self.name

    @property
    def avg_rate(self):
        return CourseComment.objects.filter(course=self).aggregate(Avg('rate'))['rate__avg']

    @property
    def amount_of_comments(self):
        return CourseComment.objects.filter(course=self).count()

    def save(self, *args, **kwargs):
        if self.video_link:
            current_video_link = self.video_link
            video_id = current_video_link
            if "embed" in current_video_link:
                video_id = current_video_link.split('embed/')[1].split(" ")[0][:-1]
            elif "v=" in current_video_link:
                video_id = current_video_link.split('v=')[1].split('&')[0]
            self.video_link = video_id
        super(Course, self).save(*args, **kwargs)


class HomeCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    position = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return str(self.position)

# class ImageSubject(models.Model):
#     course = models.ForeignKey(Subject, related_name='main_photo', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='subject_images/')
    #default = models.BooleanField(default=False)
    #different_name.admin_order_field = 'dfname'
    # def save(self):
    #     super().save()
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 420 or img.width > 350:
    #         output_size = (420, 350)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)



# class Teacher(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     short_biography = models.TextField(null=True)
#     position = models.CharField(max_length=150, null=True)
#     image = models.ImageField(upload_to='teachers_images/', default='teachers_images/default.png',)
#     rating = models.FloatField(null=True)
#
#     def __str__(self):
#         full_name = self.first_name + ' ' + self.last_name
#         return full_name


    # def save(self):
    #     super().save()
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 420 or img.width > 350:
    #         output_size = (420, 350)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)



# class Course(models.Model):
#     price = models.IntegerField(default=0)
#     teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
#
#     def __str__(self):
#         text = self.subject.name + ' by ' + str(self.teacher) + ': Price - ' + str(self.price) + '$'
#         return text

class ApplicantNotRegistered(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class ApplicationFromHome(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    info_text = models.TextField()
    ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class CourseParticipant(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        text = self.student.user.username + ' participation in ' + self.course.subject.name
        return text


class TeacherComment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    writer = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=350, blank=True)
    rate = models.IntegerField(default=5)
    ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        text = self.writer.user.username + ' about ' + self.teacher.user.username
        return text

class CourseComment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    writer = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=350, blank=True)
    rate = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        text = self.writer.user.username + ' about ' + self.course.name
        return text