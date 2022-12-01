from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm, LessonForm, ScheduleForm, ChildrenForm, PaymentForm
from .forms import DateForm
from .models import User, Lesson, Children, TermDates, Schedule, Payment
from django.db.models import Prefetch

from datetime import datetime
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar
# Create your views here.


class CalendarView(generic.ListView):
    model = Schedule
    template_name = 'teacher_landing_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(self.request.user, d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def home(request):
    return render(request, 'home.html')

def student_landing_page(request):
    if request.method == "POST":
        form = LessonForm(data=request.POST, request=request)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.user = request.user
            lesson.invoiceEmail = request.user.email
            lesson.save()
            return redirect('student_landing_page')
    else:
        form = LessonForm(request=request)
    return render(request, 'student_landing_page.html', {'form': form})


'''Checks if the user is logged in.If not,
sends them back to the home page.If they are,
all of their lessons are assigned to lesson
list and then sends them to the lesson page'''


def student_lessons(request):
    if request.user.is_authenticated:
        currentUser = request.user
        asChild = Children.objects.filter(email=currentUser.email)
        myChildrenEmail = Children.objects.filter(parent=currentUser).values('email')
        if myChildrenEmail.exists():
            allChildren = Children.objects.filter(email__in=myChildrenEmail)
        else:
            allChildren = Children.objects.none()
        childUser = User.objects.filter(email__in=myChildrenEmail)
        lessonsList = Lesson.objects.filter(user=currentUser) | Lesson.objects.filter(
            children__in=asChild) | Lesson.objects.filter(children__in=allChildren) | Lesson.objects.filter(user__in=childUser)
        return render(request, 'student_lessons.html', {'student_lessons': lessonsList})
    else:
        return render(request, 'home.html')


def admin_lessons(request):
    lessonsList = Lesson.objects.all()
    return render(request, 'admin_lessons.html', {'admin_lessons': lessonsList})

# Delete a lessons


def delete_lesson(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    lesson.delete()
    if request.user.is_authenticated:
        currentUser = request.user
        asChild = Children.objects.filter(email=currentUser.email)
        myChildrenEmail = Children.objects.filter(parent=currentUser).values('email')
        if myChildrenEmail.exists():
            allChildren = Children.objects.filter(email__in=myChildrenEmail)
        else:
            allChildren = Children.objects.none()
        childUser = User.objects.filter(email__in=myChildrenEmail)
        lessonsList = Lesson.objects.filter(user=currentUser) | Lesson.objects.filter(
            children__in=asChild) | Lesson.objects.filter(children__in=allChildren) | Lesson.objects.filter(user__in=childUser)
        return render(request, 'student_lessons.html', {'student_lessons': lessonsList})
    else:
        return render(request, 'home.html')

# Edits lessons


def edit_lesson(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    form = LessonForm(data=request.POST or None, request=request, instance=lesson)
    if form.is_valid():
        lesson = form.save(commit=False)
        lesson.user = request.user
        lesson.save()
        currentUser = request.user
        asChild = Children.objects.filter(email=currentUser.email)
        myChildrenEmail = Children.objects.filter(parent=currentUser).values('email')
        if myChildrenEmail.exists():
            allChildren = Children.objects.filter(email__in=myChildrenEmail)
        else:
            allChildren = Children.objects.none()
        childUser = User.objects.filter(email__in=myChildrenEmail)
        lessonsList = Lesson.objects.filter(user=currentUser) | Lesson.objects.filter(
            children__in=asChild) | Lesson.objects.filter(children__in=allChildren) | Lesson.objects.filter(user__in=childUser)
        return render(request, 'student_lessons.html', {'student_lessons': lessonsList})
    return render(request, 'update_lessons.html',
                  {'lesson': lesson,
                   'form': form})


def book_lesson(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    form = ScheduleForm(data=request.POST or None, request=request)
    if form.is_valid():
        schedule = form.save(commit=False)
        schedule.lesson = lesson
        schedule.save()
        lesson.is_confirmed = True
        lesson.lessons = schedule.number_of_lessons
        lesson.duration = schedule.duration
        if schedule.interval == '7':
            lesson.desiredInterval = 'Once a week'
        elif schedule.interval == '14':
            lesson.desiredInterval = 'Once every two weeks'
        elif schedule.interval == '30':
            lesson.desiredInterval = 'Once a month'
        lesson.save()
        user = lesson.user
        lessonCost = 20
        totalCost = lessonCost*schedule.number_of_lessons
        user.outstanding_balance += totalCost
        user.save()
        lessonsList = Lesson.objects.all()
        return render(request, 'admin_lessons.html', {'admin_lessons': lessonsList})
    return render(request, 'book_lessons.html',
                  {'lesson': lesson,
                   'form': form})


def edit_booking(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    schedule = Schedule.objects.get(lesson = lesson)
    lessonCost = 20
    initialLessons = schedule.number_of_lessons
    initialCost = lessonCost*initialLessons
    form = ScheduleForm(data=request.POST or None, instance=schedule, request=request)
    if form.is_valid():
        schedule = form.save(commit=False)
        schedule.save()
        lesson.lessons = schedule.number_of_lessons
        lesson.duration = schedule.duration
        if schedule.interval == '7':
            lesson.desiredInterval = 'Once a week'
        elif schedule.interval == '14':
            lesson.desiredInterval = 'Once every two weeks'
        elif schedule.interval == '30':
            lesson.desiredInterval = 'Once a month'
        lesson.save()
        newLessons = schedule.number_of_lessons
        user = lesson.user
        if newLessons < initialLessons:
            differenceCost = initialCost - (lessonCost*newLessons)
            user.outstanding_balance -= differenceCost
        elif newLessons > initialLessons:
            differenceCost = (lessonCost*newLessons) - initialCost
            user.outstanding_balance += differenceCost
        user.save()
        lessonsList = Lesson.objects.all()
        return render(request, 'admin_lessons.html', {'admin_lessons': lessonsList})
    return render(request, 'update_bookings.html',
                  {'lesson': lesson,
                   'form': form})


def delete_booking(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    schedule = Schedule.objects.get(lesson=lesson)
    lessonCost = 20
    totalCost = lessonCost*schedule.number_of_lessons
    user = lesson.user
    user.outstanding_balance -= totalCost
    user.save()
    lesson.delete()
    schedule.delete()
    lessonsList = Lesson.objects.all()
    return render(request, 'admin_lessons.html', {'admin_lessons': lessonsList})


def add_children(request):
    if request.method == "POST":
        form = ChildrenForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = request.user
            child.save()
            return redirect('my_children')
    else:
        form = ChildrenForm()
    return render(request, 'add_children.html', {'form': form})


def my_children(request):
    if request.user.is_authenticated:
        currentUser = request.user
        childrenList = Children.objects.filter(parent=currentUser)
        return render(request, 'my_children.html', {'my_children': childrenList})
    else:
        return render(request, 'home.html')


def delete_children(request, childrenId):
    child = Children.objects.get(id=childrenId)
    child.delete()
    if request.user.is_authenticated:
        currentUser = request.user
        childrenList = Children.objects.filter(parent=currentUser)
        return render(request, 'my_children.html', {'my_children': childrenList})
    else:
        return render(request, 'home.html')


def student_payment(request):
    if request.user.is_authenticated:
        currentUser = request.user
        paymentList = Payment.objects.filter(student=currentUser).order_by('-payment_time')
        return render(request, 'student_payment.html', {'student': currentUser, 'student_payment': paymentList})
    else:
        return render(request, 'home.html')

def admin_landing_page(request):
    return render(request, 'admin_landing_page.html')


def admin_payment(request):
    studentList = User.objects.filter(is_teacher = False, is_staff = False, is_superuser = False)
    return render(request, 'admin_payment.html', {'admin_payment': studentList})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_landing_page')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    return redirect('admin_landing_page')
                if user.is_teacher:
                    login(request, user)
                    return redirect('teacher_landing_page')
                login(request, user)
                return redirect('student_landing_page')
        # Add error message here
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})


def term_dates(request):
    form = DateForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            terms = TermDates.objects.all()
            return redirect('view_term_dates')
    return render(request, 'term_dates.html', {'form':form})

def view_term_dates(request):
    terms = TermDates.objects.all()
    return render(request, 'view_term_dates.html', {"term_dates":terms})

def edit_term_dates(request, term_id):
    term = TermDates.objects.get(pk=term_id)
    form = DateForm(data=request.POST or None, instance = term)
    if form.is_valid():
        term = form.save(commit=False)
        term.save()
        terms = TermDates.objects.all()
        return render(request, 'view_term_dates.html', {"term_dates":terms})
    terms = TermDates.objects.all()
    return render(request, 'edit_term.html', {"term_dates":terms, 'form':form})

def delete_term_dates(request, term_id):
    term = TermDates.objects.get(pk=term_id)
    term.delete()
    terms = TermDates.objects.all()
    return render(request, 'view_term_dates.html', {"term_dates":terms})

def log_out(request):
    logout(request)
    return redirect('home')

# pdf generator for invoice.


def invoice_generator(request, lessonId):
    currentUser = request.user
    currentLesson = Lesson.objects.get(id=lessonId)
    currentSchedule = Schedule.objects.get(lesson=currentLesson)
    lessonCost = 20
    totalCost = lessonCost*currentSchedule.number_of_lessons
    if currentLesson.invoiceNum == 'default':
        currentLesson.invoiceNum = (str(currentUser.pk)[:4]).zfill(4) + "-" + (str(currentLesson.pk)[:4]).zfill(4)
        currentLesson.save()
    if currentLesson.studentNum == 'default':
        currentLesson.studentNum = (str(currentUser.pk)[:4]).zfill(4)
        currentLesson.save()
    if(currentLesson.children is not None):
        first_name = currentLesson.children.first_name;
        last_name = currentLesson.children.last_name;
    else:
        first_name = currentUser.first_name;
        last_name = currentUser.last_name;

    information = {
        "first_name": first_name,
        "last_name": last_name,
        "email_address": currentLesson.invoiceEmail,
        "Student_Id": currentLesson.studentNum,
        "Invoice_Id": currentLesson.invoiceNum,
        "Lesson_type": "Type of Instrument",
        "Number_of_lessons": currentSchedule.number_of_lessons,
        "Cost_per_lesson": lessonCost,
        "Total_cost": totalCost,
        "Invoice_dateAndTime": currentSchedule.time_stamp,
    }
    return render(request, 'invoices.html', information)

def lesson_detail_generator(request, lessonId):
    currentLesson = Lesson.objects.get(id=lessonId)
    currentSchedule = Schedule.objects.get(lesson=currentLesson)
    information = {
        "Number_of_lessons": currentSchedule.number_of_lessons,
        "Start_date": currentSchedule.start_date,
        "Start_time": currentSchedule.start_time,
        "Interval": currentSchedule.interval,
        "Duration":currentSchedule.duration,
        "Teacher":currentSchedule.teacher
    }
    return render(request, 'student_timetable.html', information)

def make_payment(request, userId):
    student = User.objects.get(id=userId)
    form = PaymentForm(data=request.POST or None)
    if form.is_valid():
        payment = form.save(commit=False)
        payment.student = student
        payment.save()
        amount_paid = payment.amount_paid
        payment.balance_before = student.outstanding_balance
        student.outstanding_balance -= amount_paid
        student.save()
        payment.balance_after = student.outstanding_balance
        payment.save()
        studentList = User.objects.filter(is_teacher = False, is_staff = False, is_superuser = False)
        return render(request, 'admin_payment.html', {'admin_payment': studentList})
    return render(request, 'make_payment.html',
                  {'student': student,
                   'form': form})
