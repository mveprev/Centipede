from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.db.models import Prefetch
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta, date
from .forms import SignUpForm, LogInForm, LessonForm, ScheduleForm, ChildrenForm, PaymentForm
from .forms import DateForm
from .models import User, Lesson, Children, TermDates, Schedule, Payment
from .utils import Calendar
import calendar

'''Render the home page with a log in form'''


def home(request):
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
    return render(request, 'home.html', {'form': form})


'''Render the sign up pages (student sign up)'''


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


'''For all user: log out'''


def log_out(request):
    logout(request)
    return redirect('home')


'''
Function to create a list of lessons of:
- Lesson booked by user (for himself)
- Lesson booked by user (for his children)
- Lesson booked by user's children (for himself)
- Lesson booked by user's children's other parent (for these children)
'''


def createLessonList(currentUser):
    asChild = Children.objects.filter(email=currentUser.email)
    myChildrenEmail = Children.objects.filter(parent=currentUser).values('email')
    if myChildrenEmail.exists():
        allChildren = Children.objects.filter(email__in=myChildrenEmail)
    else:
        allChildren = Children.objects.none()
    childUser = User.objects.filter(email__in=myChildrenEmail)
    lessonsList = Lesson.objects.filter(user=currentUser) | Lesson.objects.filter(
        children__in=asChild) | Lesson.objects.filter(children__in=allChildren) | Lesson.objects.filter(user__in=childUser)
    return lessonsList


'''For student user: ender the landing page with a form, to request a lesson'''


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


'''For student user: show a list of lessons'''


def student_lessons(request):
    if request.user.is_authenticated:
        lessonsList = createLessonList(request.user)
        return render(request, 'student_lessons.html', {'student_lessons': lessonsList})
    else:
        return render(request, 'home.html')


'''For student user: show the balance of user and a list of payment'''


def student_payment(request):
    if request.user.is_authenticated:
        currentUser = request.user
        paymentList = Payment.objects.filter(student=currentUser).order_by('-payment_time')
        return render(request, 'student_payment.html', {'student': currentUser, 'student_payment': paymentList})
    else:
        return render(request, 'home.html')


'''For student user: edit the lesson with the form'''


def edit_lesson(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    form = LessonForm(data=request.POST or None, request=request, instance=lesson)
    if form.is_valid():
        lesson = form.save(commit=False)
        lesson.user = request.user
        lesson.save()
        lessonsList = createLessonList(request.user)
        return render(request, 'student_lessons.html', {'student_lessons': lessonsList})
    return render(request, 'update_lessons.html', {'lesson': lesson, 'form': form})


'''For student user: delete the lesson'''


def delete_lesson(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    lesson.delete()
    if request.user.is_authenticated:
        lessonsList = createLessonList(request.user)
        return render(request, 'student_lessons.html', {'student_lessons': lessonsList})
    else:
        return render(request, 'home.html')


'''For student user: renew the lesson for next term'''


def renew_lesson(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    terms = TermDates.objects.all()
    newKey = lesson.term.pk + 1
    if terms.filter(id=newKey).exists() == False:
        messages.add_message(request, messages.ERROR, "There is no further term")
    else:
        lesson.id = None
        lesson.term = terms.get(id=newKey)
        lesson.is_confirmed = False
        lesson.save()
    lessonsList = createLessonList(request.user)
    return render(request, 'student_lessons.html', {'student_lessons': lessonsList})


'''For student user: add children with a form'''


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


'''For student user: show a list of their children'''


def my_children(request):
    if request.user.is_authenticated:
        currentUser = request.user
        childrenList = Children.objects.filter(parent=currentUser)
        return render(request, 'my_children.html', {'my_children': childrenList})
    else:
        return render(request, 'home.html')


'''For student user: delete their children'''


def delete_children(request, childrenId):
    child = Children.objects.get(id=childrenId)
    child.delete()
    if request.user.is_authenticated:
        currentUser = request.user
        childrenList = Children.objects.filter(parent=currentUser)
        return render(request, 'my_children.html', {'my_children': childrenList})
    else:
        return render(request, 'home.html')


'''For admin user: render the landing page'''


def admin_landing_page(request):
    return render(request, 'admin_landing_page.html')


'''For admin user: render the lesson page with a list of all lessons'''


def admin_lessons(request):
    lessonsList = Lesson.objects.all().order_by('is_confirmed', '-id')
    return render(request, 'admin_lessons.html', {'admin_lessons': lessonsList})


'''For admin user: fulfil the lesson request with a form'''


def book_lesson(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    form = ScheduleForm(data=request.POST or None)
    if form.is_valid():
        schedule = form.save(commit=False)
        schedule.lesson = lesson
        schedule.save()
        for i in range(1, schedule.number_of_lessons):
            newSchedule = Schedule.objects.create(
                teacher=schedule.teacher,
                lesson=schedule.lesson,
                start_time=schedule.start_time,
                start_date=schedule.start_date + timedelta(days=i*schedule.interval),
                interval=schedule.interval,
                number_of_lessons=schedule.number_of_lessons,
                duration=schedule.duration,
            )
            newSchedule.save()
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
        user.outstanding_balance -= totalCost
        user.save()
        lessonsList = Lesson.objects.all()
        return render(request, 'admin_lessons.html', {'admin_lessons': lessonsList})
    return render(request, 'book_lessons.html', {'lesson': lesson, 'form': form})


'''For admin user: edit the booked lessons with a form'''


def edit_booking(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    schedules = Schedule.objects.filter(lesson=lesson)
    schedule = schedules.first()
    lessonCost = 20
    initialLessons = schedule.number_of_lessons
    initialCost = lessonCost*initialLessons
    form = ScheduleForm(data=request.POST or None, instance=schedule)
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
            user.outstanding_balance += differenceCost
        elif newLessons > initialLessons:
            differenceCost = (lessonCost*newLessons) - initialCost
            user.outstanding_balance -= differenceCost
        user.save()
        i = 0
        for x in schedules:
            x.teacher = schedule.teacher
            x.lesson = schedule.lesson
            x.start_time = schedule.start_time
            x.start_date = schedule.start_date + timedelta(days=i*schedule.interval)
            x.interval = schedule.interval
            x.number_of_lessons = schedule.number_of_lessons
            x.duration = schedule.duration
            x.save()
            i += 1
        lessonsList = Lesson.objects.all()
        return render(request, 'admin_lessons.html', {'admin_lessons': lessonsList})
    return render(request, 'update_bookings.html', {'lesson': lesson, 'form': form})


'''For admin user: delete the booked lessons'''


def delete_booking(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    schedules = Schedule.objects.filter(lesson=lesson)
    schedule = schedules.first()
    lessonCost = 20
    totalCost = lessonCost*schedule.number_of_lessons
    user = lesson.user
    user.outstanding_balance += totalCost
    user.save()
    lesson.delete()
    schedules.delete()
    lessonsList = Lesson.objects.all()
    return render(request, 'admin_lessons.html', {'admin_lessons': lessonsList})


'''For admin user: reject the request'''


def reject_booking(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    lesson.delete()
    lessonsList = Lesson.objects.all()
    return render(request, 'admin_lessons.html', {'admin_lessons': lessonsList})


'''For admin user: render the payment page with a list of payment'''


def admin_payment(request):
    studentList = User.objects.filter(is_teacher=False, is_staff=False, is_superuser=False).order_by('first_name')
    return render(request, 'admin_payment.html', {'admin_payment': studentList})


'''For admin user: add term date with a form'''


def term_dates(request):
    form = DateForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            terms = TermDates.objects.all()
            return redirect('view_term_dates')
    return render(request, 'term_dates.html', {'form': form})


'''For admin user: render the term date page with a list of terms'''


def view_term_dates(request):
    terms = TermDates.objects.all()
    return render(request, 'view_term_dates.html', {"term_dates": terms})


'''For admin user: edit the term date with a form'''


def edit_term_dates(request, term_id):
    term = TermDates.objects.get(pk=term_id)
    form = DateForm(data=request.POST or None, instance=term)
    if form.is_valid():
        term = form.save(commit=False)
        term.save()
        terms = TermDates.objects.all()
        return render(request, 'view_term_dates.html', {"term_dates": terms})
    terms = TermDates.objects.all()
    return render(request, 'edit_term.html', {"term_dates": terms, 'form': form})


'''For admin user: delete the term dates'''


def delete_term_dates(request, term_id):
    term = TermDates.objects.get(pk=term_id)
    term.delete()
    terms = TermDates.objects.all()
    return render(request, 'view_term_dates.html', {"term_dates": terms})


'''For admin user: make payment for student with a form'''


def make_payment(request, userId):
    student = User.objects.get(id=userId)
    form = PaymentForm(data=request.POST or None)
    if form.is_valid():
        payment = form.save(commit=False)
        payment.student = student
        payment.save()
        amount_paid = payment.amount_paid
        payment.balance_before = student.outstanding_balance
        student.outstanding_balance += amount_paid
        student.save()
        payment.balance_after = student.outstanding_balance
        payment.save()
        studentList = User.objects.filter(is_teacher=False, is_staff=False, is_superuser=False)
        return render(request, 'admin_payment.html', {'admin_payment': studentList})
    return render(request, 'make_payment.html',
                  {'student': student,
                   'form': form})


'''For student user: generate the invoice PDF'''


def invoice_generator(request, lessonId):
    currentUser = request.user
    currentLesson = Lesson.objects.get(id=lessonId)
    schedules = Schedule.objects.filter(lesson=currentLesson)
    currentSchedule = schedules.first()
    if currentLesson.duration == 30:
        lessonCost = 30
    elif currentLesson.duration == 45:
        lessonCost = 45
    elif currentLesson.duration == 60:
        lessonCost = 60
    totalCost = lessonCost*currentSchedule.number_of_lessons
    if currentLesson.invoiceNum == 'default':
        currentLesson.invoiceNum = (str(currentUser.pk)[:4]).zfill(
            4) + "-" + (str(currentLesson.pk)[:4]).zfill(4)
        currentLesson.save()
    if currentLesson.studentNum == 'default':
        currentLesson.studentNum = (str(currentUser.pk)[:4]).zfill(4)
        currentLesson.save()
    if(currentLesson.children is not None):
        first_name = currentLesson.children.first_name
        last_name = currentLesson.children.last_name
    else:
        first_name = currentUser.first_name
        last_name = currentUser.last_name

    information = {
        "first_name": first_name,
        "last_name": last_name,
        "email_address": currentLesson.invoiceEmail,
        "Student_Id": currentLesson.studentNum,
        "Invoice_Id": currentLesson.invoiceNum,
        "Lesson_type": "Music Lesson",
        "Number_of_lessons": currentSchedule.number_of_lessons,
        "Cost_per_lesson": lessonCost,
        "Total_cost": totalCost,
        "Invoice_dateAndTime": currentSchedule.time_stamp,
    }
    return render(request, 'invoices.html', information)


'''For student user: generate the booked lesson detail PDF'''


def lesson_detail_generator(request, lessonId):
    currentLesson = Lesson.objects.get(id=lessonId)
    schedules = Schedule.objects.filter(lesson=currentLesson)
    currentSchedule = schedules.first()
    information = {
        "Number_of_lessons": currentSchedule.number_of_lessons,
        "Start_date": currentSchedule.start_date,
        "Start_time": currentSchedule.start_time,
        "Interval": currentSchedule.interval,
        "Duration": currentSchedule.duration,
        "Teacher": currentSchedule.teacher.first_name + " " + currentSchedule.teacher.last_name,
        "Teacher_Email": currentSchedule.teacher
    }
    return render(request, 'student_timetable.html', information)


'''Render the calendar'''


class CalendarView(generic.ListView):
    model = Schedule
    template_name = 'teacher_landing_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(self.request.user, d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


'''Function used to change to the previous month in the calendar'''


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


'''Function used to change to the next month in the calendar'''


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


'''Function used to return the date'''


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()
