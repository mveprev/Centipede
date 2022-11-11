from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect,render
from .forms import SignUpForm, LogInForm

# Create your views here.
def home(request):
    return render(request,'home.html')

def landing_page(request):
    return render(request, 'landing_page.html')

def lessons(request):
    return render(request, 'lessons.html')

def payment(request):
    return render(request, 'payment.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('landing_page')
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
                login(request, user)
                return redirect('landing_page')
        #Add error message here
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid")
    form = LogInForm()
    return render(request, 'log_in.html', {'form':form})

def log_out(request):
    logout(request)
    return redirect('home')
