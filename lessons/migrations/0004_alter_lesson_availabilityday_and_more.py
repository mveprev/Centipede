# Generated by Django 4.1.3 on 2022-11-25 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_alter_lesson_availabilityday_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='availabilityDay',
            field=models.CharField(max_length=1),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='availabilityTime',
            field=models.CharField(max_length=1),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='desiredInterval',
            field=models.CharField(max_length=1),
        ),
    ]
