# Generated by Django 2.2.12 on 2021-06-10 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210610_2044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='description2',
        ),
    ]