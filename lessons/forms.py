from django.core.validators import validate_email
from django.core.validators import RegexValidator
from django import forms
from lessons.models import User, Children, TermDates
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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

    class Meta:
        model = Lesson
        fields = ('children','lessons','availability','desiredInterval','duration','furtherInfo','id')

    INTERVAL_CHOICES= [
    ('',''),
    ('1', '1 LESSON EVERY 2 WEEK'),
    ('2', '1 LESSON EVERY 2 WEEKS'),
    ]

    DURATION_CHOICES= [
    ('',''),
    ('30', '30'),
    ('45', '45'),
    ('60', '60'),
    ]

    children = CustomLessonForm(
        queryset=None,
        empty_label='------------ I am booking lessons for myself ------------',
        required=False,
        widget=forms.Select,
        label=mark_safe("<strong>Select Children</strong>")
    )

    availability=forms.IntegerField(label=mark_safe("<strong>Enter availability</strong>"))

    lessons= forms.IntegerField(label=mark_safe("<strong>Enter the number of lessons</strong>"))

    desiredInterval=forms.IntegerField(label=mark_safe("<strong>Enter desired interval between lessons</strong>"),
    widget=forms.Select(choices=INTERVAL_CHOICES))

    duration=forms.IntegerField(label=mark_safe("<strong>Enter duration of the lesson</strong>"),
    widget=forms.Select(choices=DURATION_CHOICES))

    furtherInfo=forms.CharField(label=mark_safe("<strong>Add any further information below( (e.g. what do you want to learn or the name of a teacher if you have one in mind)</strong>"),
    widget=forms.Textarea(attrs={'rows':5, 'cols':60}))

class BookingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(BookingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Lesson
        fields = ('lessons','availability','desiredInterval','duration','furtherInfo','id')

    INTERVAL_CHOICES= [
    ('',''),
    ('1', '1 LESSON EVERY 2 WEEK'),
    ('2', '1 LESSON EVERY 2 WEEKS'),
    ]

    DURATION_CHOICES= [
    ('',''),
    ('30', '30'),
    ('45', '45'),
    ('60', '60'),
    ]

    availability=forms.IntegerField(label=mark_safe("<strong>Enter availability</strong>"))

    lessons= forms.IntegerField(label=mark_safe("<strong>Enter the number of lessons</strong>"))

    desiredInterval=forms.IntegerField(label=mark_safe("<strong>Enter the interval between lessons</strong>"),
    widget=forms.Select(choices=INTERVAL_CHOICES))

    duration=forms.IntegerField(label=mark_safe("<strong>Enter duration of the lesson</strong>"),
    widget=forms.Select(choices=DURATION_CHOICES))

    furtherInfo=forms.CharField(label=mark_safe("<strong>Add any further information below</strong>"),
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

class DateForm(forms.ModelForm):
    class Meta:
        model = TermDates
        fields = ('start_date', 'end_date')
    
    
    
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


    