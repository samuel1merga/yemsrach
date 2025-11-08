from django.shortcuts import render, redirect
from .models import news, User, saved
from django.http import HttpResponse, HttpResponseForbidden
from functools import wraps
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def create_admin(request):
    User.objects.create_user(
        username='sami',
        password='sami',
        role='admin',
        email='sami@example.com',
    )
    return HttpResponse("Admin user 'sami' created successfully!")


def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in.")
            
            if request.user.role not in allowed_roles:
                return HttpResponseForbidden("You do not have permission to access this page.")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            if user.role == 'admin': return redirect('send_news')

        messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def home(request):
    all_news = news.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'news': all_news})

def about(request):
    
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        lname = request.POST.get('lname')
        ph_no = request.POST.get('phone_no')
        pp = request.FILES.get('profile_picture')
        location = request.POST.get('location')

        if saved.objects.filter(fname=fname,mname=mname,lname=lname).exists():
            return redirect('register')
        saved.objects.create(
            fname = fname,
            mname = mname,
            phone_no = ph_no,
            lname = lname,
            profile_picture = pp,
            location = location,
        )
        return redirect('home')
    return render(request, 'register.html')
@login_required
@role_required(allowed_roles=['admin'])
def send_news(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        if message:
            # Get the oldest news object (if it exists)
            oldest_news = news.objects.order_by('created_at').first()
            
            # If there are already 2 news objects, delete the oldest one
            if news.objects.count() >= 2:
                oldest_news.delete()
            
            # Create a new news object
            news.objects.create(
                title=title,
                new=message,
            )
            return redirect('home')
    return render(request, 'news.html')


@login_required
@role_required(allowed_roles=['admin'])
def view_saved(request):
    saveds = saved.objects.all().order_by('-registered_at')
    return render(request, 'saved_file.html', {'saved': saveds})