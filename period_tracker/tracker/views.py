from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout  # Make sure authenticate and login are imported
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import PeriodLog, UserProfile
from .forms import UserProfileForm  

# Home Page
def home(request):
    return render(request, 'home.html')

# User Signup
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()

        # Validate input
        if not username or not password or not email:
            messages.error(request, "All fields are required.")
            return redirect('signup')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Choose a different one.")
            return redirect('signup')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Create user profile
        UserProfile.objects.create(user=user)

        messages.success(request, "Signup successful! You can now log in.")
        return redirect('login')

    return render(request, 'signup.html')

# User Login
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

# User Logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

# Dashboard
@login_required
def dashboard(request):
    periods = PeriodLog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'dashboard.html', {'periods': periods})

# Track Period
@login_required
def track_period(request):
    if request.method == "POST":
        start_date_str = request.POST.get('start_date', '')
        cycle_length = request.POST.get('cycle_length', '28').strip()  # Default 28 days

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            cycle_length = int(cycle_length)
            
            # Call log_period to handle the period logging logic
            log_period(request.user, start_date, cycle_length)

            messages.success(request, "Period logged successfully!")
            return redirect('dashboard')

        except ValueError:
            messages.error(request, "Invalid date format. Please enter a valid date.")
            return redirect('track_period')

    return render(request, 'track_period.html')

# Log Period - Separate function
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PeriodLog
from datetime import datetime, timedelta

def log_period(request):
    if request.method == "POST":
        start_date_str = request.POST.get('start_date', '')
        cycle_length = request.POST.get('cycle_length', '28')  # Default to 28 if not provided

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            cycle_length = int(cycle_length)
            next_period_date = start_date + timedelta(days=cycle_length)

            # Create or update period log for the user
            log_period, created = PeriodLog.objects.update_or_create(
                user=request.user,
                date=start_date,
                defaults={'cycle_length': cycle_length, 'next_period_date': next_period_date}
            )

            return redirect('new')  # Redirect to dashboard after saving the period
        except ValueError:
            messages.error(request, "Invalid date format. Please enter a valid date.")
            return redirect('log_period')

    # If GET request, show the form for entering period details
    return render(request, 'log.html')

def new(request):
    # Get all periods for the logged-in user
    periods = PeriodLog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'new.html', {'periods': periods})
    
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

# Settings View
def settings_view(request):
    # Your logic for the settings page
    return render(request, 'settings.html')