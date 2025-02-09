from django.utils.timezone import now
from django.core.mail import send_mail
from .models import PeriodTracker

from django.utils.timezone import now
from django.core.mail import send_mail
from .models import PeriodTracker

def send_period_reminders():
    today = now().date()
    upcoming_periods = PeriodTracker.objects.filter(
        next_period_date=today + timedelta(days=2),  # Two days before the period
        reminder_sent=False
    )

    for period in upcoming_periods:
        user_email = period.user.email
        if user_email:
            send_mail(
                "Upcoming Period Reminder",
                f"Hello {period.user.username}, your period is expected to start on {period.next_period_date}. Please take care!",
                "noreply@periodtracker.com",  # Replace with your email
                [user_email],
                fail_silently=False,
            )
            # Mark reminder as sent
            period.reminder_sent = True
            period.save()
