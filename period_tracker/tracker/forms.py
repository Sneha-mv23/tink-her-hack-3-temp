from django import forms
from django.contrib.auth.models import User
from .models import PeriodTracker, UserProfile


 
class PeriodTrackerForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Start Date"
    )
    duration = forms.IntegerField(
        min_value=1,
        max_value=60,
        label="Cycle Duration (Days)"
    )

    class Meta:
        model = PeriodTracker
        fields = ['start_date', 'duration']


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label="Email"
    )  # Added email field
    
    age = forms.IntegerField(
        min_value=10,
        max_value=100,
        required=False,
        label="Age"
    )
    weight = forms.FloatField(
        min_value=30.0,
        max_value=200.0,
        required=False,
        label="Weight (kg)"
    )
    cycle_length = forms.IntegerField(
        min_value=21,
        max_value=35,
        label="Average Cycle Length (Days)"
    )

    class Meta:
        model = UserProfile
        fields = ['age', 'weight', 'cycle_length']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['email'].initial = self.instance.user.email  # Prefill email

    def save(self, commit=True):
        user = self.instance.user
        user.email = self.cleaned_data['email']  # Save email to User model
        user.save()
        return super().save(commit)
