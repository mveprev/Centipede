# Generated by Django 4.1.3 on 2022-12-07 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import lessons.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('is_teacher', models.BooleanField(default=False, verbose_name='teacher')),
                ('is_staff', models.BooleanField(default=False, verbose_name='administrator')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='director')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('outstanding_balance', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', lessons.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Children',
            fields=[
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('mondayMorning', models.BooleanField(default=False)),
                ('mondayAfternoon', models.BooleanField(default=False)),
                ('mondayNight', models.BooleanField(default=False)),
                ('tuesdayMorning', models.BooleanField(default=False)),
                ('tuesdayAfternoon', models.BooleanField(default=False)),
                ('tuesdayNight', models.BooleanField(default=False)),
                ('wednesdayMorning', models.BooleanField(default=False)),
                ('wednesdayAfternoon', models.BooleanField(default=False)),
                ('wednesdayNight', models.BooleanField(default=False)),
                ('thursdayMorning', models.BooleanField(default=False)),
                ('thursdayAfternoon', models.BooleanField(default=False)),
                ('thursdayNight', models.BooleanField(default=False)),
                ('fridayMorning', models.BooleanField(default=False)),
                ('fridayAfternoon', models.BooleanField(default=False)),
                ('fridayNight', models.BooleanField(default=False)),
                ('lessons', models.IntegerField()),
                ('desiredInterval', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('furtherInfo', models.TextField()),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('invoiceNum', models.CharField(default='default', max_length=50)),
                ('studentNum', models.CharField(default='default', max_length=50)),
                ('invoiceEmail', models.CharField(default='default', max_length=50)),
                ('children', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lessons.children')),
            ],
        ),
        migrations.CreateModel(
            name='TermDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='default', max_length=50, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(auto_now=True)),
                ('start_time', models.TimeField()),
                ('start_date', models.DateField()),
                ('interval', models.IntegerField()),
                ('number_of_lessons', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_time', models.DateTimeField(auto_now=True)),
                ('amount_paid', models.IntegerField()),
                ('balance_before', models.IntegerField(default=0)),
                ('balance_after', models.IntegerField(default=0)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='term',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lessons.termdates'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
