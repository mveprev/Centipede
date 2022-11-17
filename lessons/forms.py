from django.core.validators import validate_email
from django.core.validators import RegexValidator
from django import forms
from lessons.models import User
from django.utils.safestring import mark_safe

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

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('lessons','availability','desiredInterval','duration','furtherInfo','id')

    INTERVAL_CHOICES= [
    ('1', '1 LESSON EVERY 2 WEEK'),
    ('2', '1 LESSON EVERY 2 WEEKS'),
    ]

    DURATION_CHOICES= [
    ('30', '30'),
    ('45', '45'),
    ('60', '60'),
    ]

    availability=forms.IntegerField(label=mark_safe("<strong>Enter availability :</strong>"))

    lessons= forms.IntegerField(label=mark_safe("<strong>Enter the number of lessons:</strong>"))

    desiredInterval=forms.IntegerField(label=mark_safe("<strong>Enter desired interval between lessons:</strong>"),
    widget=forms.Select(choices=INTERVAL_CHOICES))


    duration=forms.IntegerField(label=mark_safe("<strong>Enter duration of the lesson:</strong>"),
    widget=forms.Select(choices=DURATION_CHOICES))

    furtherInfo=forms.CharField(label=mark_safe("<strong>Add any further information below( (e.g. what do you want to learn or the name of a teacher if you have one in mind).</strong>"),
    widget=forms.Textarea(attrs={'rows':5, 'cols':60}))
    