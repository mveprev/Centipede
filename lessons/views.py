from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect,render
from .forms import SignUpForm, LogInForm, LessonForm
from .models import User, Lesson

# Create your views here.
def home(request):
    return render(request,'home.html')

def student_landing_page(request):
    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.user=request.user
            lesson.save()
            return redirect('student_landing_page')
    else:
        form = LessonForm()
    return render(request, 'student_landing_page.html',{'form': form})

'''Checks if the user is logged in.If not,
sends them back to the home page.If they are,
all of their lessons are assigned to lesson
list and then sends them to the lesson page'''
def student_lessons(request):
    if request.user.is_authenticated:
        currentUser = request.user
        lessonsList = Lesson.objects.filter(user=currentUser)
        return render(request, 'student_lessons.html', {'student_lessons':lessonsList})
    else:
        return render(request,'home.html')

def admin_lessons(request):
    lessonsList = Lesson.objects.all()
    return render(request, 'admin_lessons.html', {'admin_lessons': lessonsList})

#Delete a lessons
def delete_lesson(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    lesson.delete()
    if request.user.is_authenticated:
        currentUser = request.user
        lessonsList = Lesson.objects.filter(user=currentUser)
        return render(request, 'student_lessons.html', {'student_lessons':lessonsList})
    else:
        return render(request,'home.html')

#Edits lessons
def edit_lesson(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    form = LessonForm(request.POST or None, instance = lesson)
    if form.is_valid():
        lesson = form.save(commit=False)
        lesson.user=request.user
        lesson.save()
        currentUser = request.user
        lessonsList = Lesson.objects.filter(user=currentUser)
        return render(request, 'student_lessons.html', {'student_lessons':lessonsList})
    return render(request, 'update_lessons.html',
    {'lesson':lesson,
    'form':form})

def book_lesson(request, lessonId):
    lesson = Lesson.objects.get(id=lessonId)
    form = LessonForm(request.POST or None, instance = lesson)
    if form.is_valid():
        lesson = form.save(commit=False)
        lesson.is_confirmed = True
        lesson.save()
        lessonsList = Lesson.objects.all()
        return render(request, 'admin_lessons.html', {'admin_lessons': lessonsList})
    return render(request, 'book_lessons.html',
    {'lesson': lesson,
    'form': form})

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
        #Add error message here
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid")
    form = LogInForm()
    return render(request, 'log_in.html', {'form':form})

def log_out(request):
    logout(request)
    return redirect('home')
