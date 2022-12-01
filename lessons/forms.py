from django.core.validators import validate_email
from django.core.validators import RegexValidator
from django import forms
from lessons.models import User, Children, TermDates, Schedule, Renewal, Payment
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

from .models import Lesson

class LogInForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name']

    email = forms.CharField(label='Email', validators=[validate_email])
    new_password = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase character, a number.'
            )]
    )
    password_confirmation = forms.CharField(label = 'Password confirmation', widget = forms.PasswordInput())

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('email'),
            first_name = self.cleaned_data.get('first_name'),
            last_name = self.cleaned_data.get('last_name'),
            password = self.cleaned_data.get('new_password')
        )
        return user


class CustomLessonForm(forms.ModelChoiceField):
    def label_from_instance(self, children):
        return children.first_name + ' ' + children.last_name


class LessonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(LessonForm, self).__init__(*args, **kwargs)
        self.fields['children'].queryset = Children.objects.filter(parent=self.request.user)
        self.fields['term'].queryset = TermDates.objects.all()

    class Meta:
        model=Lesson
        fields=('term', 'children',
            'mondayMorning','mondayAfternoon','mondayNight',
            'tuesdayMorning','tuesdayAfternoon','tuesdayNight',
            'wednesdayMorning','wednesdayAfternoon','wednesdayNight',
            'thursdayMorning','thursdayAfternoon','thursdayNight',
            'fridayMorning','fridayAfternoon','fridayNight',
            'lessons','desiredInterval','duration','furtherInfo','id',
            )

    INTERVAL_CHOICES= [
    ('',''),
    ('Once a week', 'Once a week'),
    ('Once every two weeks', 'Once every two weeks'),
    ('Once a month', 'Once a month'),
    ]

    DURATION_CHOICES= [
    ('',''),
    ('30', '30'),
    ('45', '45'),
    ('60', '60'),
    ]

    term = forms.ModelChoiceField(
        queryset=None,
        empty_label='------------ Please select term ------------',
        required=True,
        widget=forms.Select,
        label=mark_safe("<strong>Select Term</strong>")
    )

    children = CustomLessonForm(
        queryset=None,
        empty_label='------------ I am booking lessons for myself ------------',
        required=False,
        widget=forms.Select,
        label=mark_safe("<strong>Select Children</strong>")
    )

    mondayMorning=forms.BooleanField(required=False,label=mark_safe("<strong>Monday &nbsp&nbsp&nbsp&nbsp&nbsp Morning (8:00 - 12:00)</strong>"))
    mondayAfternoon=forms.BooleanField(required=False,label=mark_safe("<strong> &nbsp Afternoon (13:00 - 17:00)</strong>"))
    mondayNight=forms.BooleanField(required=False,label=mark_safe("<strong> &nbsp Night (18:00 - 22:00)</strong>"))
    tuesdayMorning=forms.BooleanField(required=False,label=mark_safe("<strong>Tuesday &nbsp&nbsp&nbsp&nbsp&nbsp Morning (8:00 - 12:00)</strong>"))
    tuesdayAfternoon=forms.BooleanField(required=False,label=mark_safe("<strong> &nbsp Afternoon (13:00 - 17:00)</strong>"))
    tuesdayNight=forms.BooleanField(required=False,label=mark_safe("<strong> &nbsp Night (18:00 - 22:00)</strong>"))
    wednesdayMorning=forms.BooleanField(required=False,label=mark_safe("<strong>Wednesday Morning (8:00 - 12:00)</strong>"))
    wednesdayAfternoon=forms.BooleanField(required=False,label=mark_safe("<strong> &nbsp Afternoon (13:00 - 17:00)</strong>"))
    wednesdayNight=forms.BooleanField(required=False,label=mark_safe("<strong> &nbsp Night (18:00 - 22:00)</strong>"))
    thursdayMorning=forms.BooleanField(required=False,label=mark_safe("<strong>Thursday &nbsp&nbsp&nbsp&nbsp Morning (8:00 - 12:00)</strong>"))
    thursdayAfternoon=forms.BooleanField(required=False,label=mark_safe("<strong> &nbsp Afternoon (13:00 - 17:00)</strong>"))
    thursdayNight=forms.BooleanField(required=False,label=mark_safe("<strong> &nbsp Night (18:00 - 22:00)</strong>"))
    fridayMorning=forms.BooleanField(required=False,label=mark_safe("<strong>Friday &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp Morning (8:00 - 12:00)</strong>"))
    fridayAfternoon=forms.BooleanField(required=False,label=mark_safe("<strong> &nbsp Afternoon (13:00 - 17:00)</strong>"))
    fridayNight=forms.BooleanField(required=False,label=mark_safe("<strong> &nbsp Night (18:00 - 22:00)</strong>"))

    lessons= forms.IntegerField(label=mark_safe("<strong>Enter the number of lessons</strong>"))
    desiredInterval=forms.CharField(label=mark_safe("<strong>Enter desired interval between lessons</strong>"),
    widget=forms.Select(choices=INTERVAL_CHOICES))
    duration=forms.IntegerField(label=mark_safe("<strong>Enter duration of the lesson</strong>"),
    widget=forms.Select(choices=DURATION_CHOICES))
    furtherInfo=forms.CharField(label=mark_safe("<strong>Add any further information below( (e.g. what do you want to learn or the name of a teacher if you have one in mind)</strong>"),
    widget=forms.Textarea(attrs={'rows':5, 'cols':60}))

class ChildrenForm(forms.ModelForm):
    class Meta:
        model = Children
        fields = ('first_name','last_name','age', 'email')

    email = forms.CharField(label='child email (optional)', validators=[validate_email], required=False)
    first_name = forms.CharField(label='child first name')
    last_name = forms.CharField(label='child last name')
    age = forms.IntegerField(label='child age')

class DatePickerInput(forms.DateInput):
    input_type = 'date'

class TimePickerInput(forms.TimeInput):
        input_type = 'time'

class DateForm(forms.ModelForm):
    class Meta:
        model = TermDates
        fields = ('name', 'start_date', 'end_date')

    start_date = forms.DateField(widget=DatePickerInput)
    end_date = forms.DateField(widget=DatePickerInput)


    def clean_start_date(self, *args, **kwargs):
        start_date = self.cleaned_data.get("start_date")
        for each in TermDates.objects.all():
            if each.start_date <= start_date <= each.end_date and self.instance.pk != each.pk:
                raise forms.ValidationError("Overlaps with other terms")
        return start_date

    def clean_end_date(self, *args, **kwargs):
        end_date = self.cleaned_data.get("end_date")
        start_date = self.cleaned_data.get("start_date")
        if start_date != None:
            if end_date <= start_date:
                raise forms.ValidationError("Range not valid")
            for each in TermDates.objects.all():
                if each.end_date >= end_date >= each.start_date and self.instance.pk != each.pk:
                    raise forms.ValidationError("Overlaps with other terms")
        return end_date

class CustomScheduleForm(forms.ModelChoiceField):
    def label_from_instance(self, user):
        return user.first_name + ' ' + user.last_name

class ScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = User.objects.filter(is_teacher=True)

    class Meta:
        model = Schedule
        fields = ('teacher','start_time','start_date','interval','number_of_lessons','duration')

    INTERVAL_CHOICES= [
    ('',''),
    ('7', 'Once a week'),
    ('14', 'Once every two weeks'),
    ('30', 'Once a month'),
    ]

    DURATION_CHOICES= [
    ('',''),
    ('30', '30'),
    ('45', '45'),
    ('60', '60'),
    ]

    teacher = CustomScheduleForm(
        queryset=None,
        empty_label='------------ Please select teacher ------------',
        required=True,
        widget=forms.Select,
        label=mark_safe("<strong>Select Teacher</strong>")
    )
    start_time = forms.TimeField(label=mark_safe("<strong>Enter the start time</strong>"),widget=TimePickerInput)
    start_date = forms.DateField(label=mark_safe("<strong>Enter the start date</strong>"),widget=DatePickerInput)
    number_of_lessons = forms.IntegerField(label=mark_safe("<strong>Enter the number of lessons</strong>"))
    interval = forms.IntegerField(label=mark_safe("<strong>Enter interval between lessons</strong>"),widget=forms.Select(choices=INTERVAL_CHOICES))
    duration = forms.IntegerField(label=mark_safe("<strong>Enter duration of the lesson</strong>"),widget=forms.Select(choices=DURATION_CHOICES))
<<<<<<< HEAD

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount_paid',)
    amount_paid = forms.IntegerField(label=mark_safe("<strong>Enter the amount paid</strong>"))
=======

#class RenewForm(forms.ModelForm):
    #class Meta:
        #model = Renewal
        #fields = ('renew')

    #renew = forms.BooleanField(label=mark_safe("<strong>Renew</strong>"))
>>>>>>> main
