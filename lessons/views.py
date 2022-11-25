from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm, LessonForm, BookingForm, ChildrenForm
from .models import User, Lesson, Children
from django.db.models import Prefetch

# Create your views here.


def home(request):
    return render(request, 'home.html')


def student_landing_page(request):
    if request.method == "POST":
        form = LessonForm(data=request.POST, request=request)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.user = request.user
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
    form = BookingForm(data=request.POST or None, request=request, instance=lesson)
    if form.is_valid():
        lesson = form.save(commit=False)
        lesson.is_confirmed = True
        lesson.save()
        lessonsList = Lesson.objects.all()
        return render(request, 'admin_lessons.html', {'admin_lessons': lessonsList})
    return render(request, 'book_lessons.html',
                  {'lesson': lesson,
                   'form': form})


def edit_booking(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    form = BookingForm(data=request.POST or None, request=request, instance=lesson)
    if form.is_valid():
        lesson = form.save(commit=False)
        lesson.save()
        lessonsList = Lesson.objects.all()
        return render(request, 'admin_lessons.html', {'admin_lessons': lessonsList})
    return render(request, 'update_bookings.html',
                  {'lesson': lesson,
                   'form': form})


def delete_booking(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    lesson.delete()
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
    return render(request, 'student_payment.html')


def admin_landing_page(request):
    return render(request, 'admin_landing_page.html')


def admin_payment(request):
    return render(request, 'admin_payment.html')


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
                login(request, user)
                return redirect('student_landing_page')
        # Add error message here
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('home')

# pdf generator for invoice.


def invoice_generator(request, lessonId):
    currentUser = request.user
    currentLesson = Lesson.objects.get(id=lessonId)
    invoiceId = (str(currentUser.pk)[:4]).zfill(4) + "-" + (str(currentLesson.pk)[:4]).zfill(4)
    lessonCost = 20
    totalCost = lessonCost*currentLesson.lessons
    information = {
        "first_name": currentUser.first_name,
        "last_name": currentUser.last_name,
        "email_address": currentUser.email,
        "Student_Id": (str(currentUser.pk)[:4]).zfill(4),
        "Invoice_Id": invoiceId,
        "Lesson_type": "Type of Instrument",
        "Number_of_lessons": currentLesson.lessons,
        "Cost_per_lesson": lessonCost,
        "Total_cost": totalCost,
    }
    return render(request, 'invoices.html', information)
