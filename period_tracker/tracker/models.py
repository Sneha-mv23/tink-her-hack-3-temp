from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class PeriodTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    duration = models.IntegerField(help_text="Cycle duration in days")  # Example: 28 days
    next_period_date = models.DateField(blank=True, null=True)
    
    
    

    def save(self, *args, **kwargs):
        """Auto-calculate next period date before saving."""
        if self.start_date and self.duration:
            self.next_period_date = self.start_date + timedelta(days=self.duration)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.start_date}"

    class Meta:
        indexes = [  # ✅ Updated index method for Django 4.2+
            models.Index(fields=['user', 'next_period_date']),
        ]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")
    cycle_length = models.IntegerField(default=28, help_text="Average cycle length in days")
    activity_level = models.CharField(
        max_length=20,
        choices=[("Low", "Low"), ("Moderate", "Moderate"), ("High", "High")],
        default="Moderate"
    )
    medical_conditions = models.TextField(blank=True, null=True, help_text="Any relevant medical conditions")

    def __str__(self):
        return f"Profile of {self.user.username}"

class PeriodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()  # Date of last period
    cycle_length = models.IntegerField(default=28)  # Default cycle length
    next_period_date = models.DateField()  # Calculated next period date

    def __str__(self):
        return f"{self.user.username} - {self.date}"