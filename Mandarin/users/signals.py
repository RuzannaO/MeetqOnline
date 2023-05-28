from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from .models import Student,Teacher


@receiver(post_save, sender=User)
def create_instance(sender, instance, created, **kwargs):
    if created:
        print(instance)
        if instance.is_teacher:
            print('teacehr')
            Teacher.objects.create(user=instance)
        else:
            print('student')
            Student.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     print('--')
#     print(instance)
#     if instance.is_teacher:
#         instance.Teacher.save()
#     else:
#         instance.Student.save()
    #instance.profile.save()