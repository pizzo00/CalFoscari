# Generated by Django 2.2.10 on 2020-04-16 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursesCalendars', '0008_auto_20200415_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='has_lessons',
            field=models.BooleanField(default=True, verbose_name='Has Lesson'),
        ),
    ]
