
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_description22'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='description22',
        ),
    ]
