from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import PeriodTracker, UserProfile
from .forms import UserProfileForm
from datetime import datetime, timedelta

# Home Page
def home(request):
    return render(request, 'home.html')

# User Signup
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        # Check if username is taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Choose a different one.")
            return redirect('signup')

        # Create new user and login
        user = User.objects.create_user(username=username, password=password)
        user.save()
        login(request, user)

        # Create user profile automatically
        UserProfile.objects.create(user=user)

        messages.success(request, "Signup successful! Profile created.")
        return redirect('dashboard')

    return render(request, 'signup.html')

# User Login
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials. Try again.")

    return render(request, 'login.html')

# User Logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

# Dashboard
@login_required
def dashboard(request):
    periods = PeriodTracker.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'dashboard.html', {'periods': periods})

# Track Period
@login_required
def track_period(request):
    if request.method == "POST":
        start_date_str = request.POST['start_date']
        duration = int(request.POST['duration'])

        # Convert start_date string to date object
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

        # Calculate next period date
        next_period_date = start_date + timedelta(days=duration)

        PeriodTracker.objects.create(
            user=request.user,
            start_date=start_date,
            duration=duration,
            next_period_date=next_period_date
        )

        messages.success(request, "Period tracked successfully!")
        return redirect('dashboard')

    return render(request, 'track_period.html')

# User Profile
@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')

    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})





