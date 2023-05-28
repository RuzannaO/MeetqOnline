# Generated by Django 3.1.5 on 2021-06-07 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantNotRegistered',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationFromHome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('info_text', models.TextField()),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('short_description', models.TextField(max_length=500)),
                ('long_description', models.TextField(blank=True, null=True)),
                ('room_type', models.CharField(choices=[('Individual', 'Individual'), ('Group', 'Group'), ('Individual/Group', 'Individual/Group')], default='Individual', max_length=25)),
                ('capacity', models.IntegerField(default=1)),
                ('topics', models.TextField()),
                ('video_link', models.CharField(blank=True, max_length=300, null=True)),
                ('price_individual', models.FloatField(blank=True, default=15, null=True)),
                ('price_group', models.FloatField(blank=True, default=10, null=True)),
                ('image', models.ImageField(upload_to='courses/')),
                ('min_age_individual', models.IntegerField(blank=True, null=True)),
                ('max_age_individual', models.IntegerField(blank=True, null=True)),
                ('min_age_group', models.IntegerField(blank=True, null=True)),
                ('max_age_group', models.IntegerField(blank=True, null=True)),
                ('duration_individual', models.CharField(blank=True, max_length=300, null=True)),
                ('duration_group', models.CharField(blank=True, max_length=300, null=True)),
                ('class_per_week_individual', models.IntegerField(blank=True, default=1, null=True)),
                ('class_per_week_group', models.IntegerField(blank=True, default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(blank=True, max_length=350)),
                ('rate', models.IntegerField(blank=True, null=True)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HomeCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='HomeSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='subjects/')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(blank=True, max_length=350)),
                ('rate', models.IntegerField(default=5)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
