# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Exercise, WorkoutDay, WorkoutDayExercise, WorkoutSession

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("As senhas não correspondem")

        return cleaned_data
    

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = [
            'name', 'description', 'use_weight', 'tip',
            'photo', 'video_url', 'rest_sec',
            'muscles', 'tags'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'tip': forms.Textarea(attrs={'rows': 2}),
            'tags': forms.CheckboxSelectMultiple(),
        }

class WorkoutDayForm(forms.ModelForm):
    class Meta:
        model = WorkoutDay
        fields = ['name', 'description', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'tags': forms.CheckboxSelectMultiple(),
        }

class WorkoutDayExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutDayExercise
        fields = ['exercise', 'order', 'custom_sets', 'custom_reps', 'rest_sec']

class WorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ['date', 'duration', 'feeling']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'duration': forms.TimeInput(attrs={'type': 'time'}),
            'feeling': forms.Select(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['duration'].widget.attrs.update({'placeholder': '01:00:00'})