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
            'photo', 'video_url', 'reps', 'sets',
            'rest_sec', 'muscles', 'tags',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'use_weight': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tip': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'reps': forms.NumberInput(attrs={'class': 'form-control'}),
            'sets': forms.NumberInput(attrs={'class': 'form-control'}),
            'rest_sec': forms.NumberInput(attrs={'class': 'form-control'}),
            'muscles': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
            'tags': forms.CheckboxSelectMultiple(
                attrs={'class': 'form-check-input'}
            ),
        }

class WorkoutDayForm(forms.ModelForm):
    class Meta:
        model = WorkoutDay
        fields = ['name', 'description', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            # O CheckboxSelectMultiple não aceita diretamente 'form-check-input' no widget,
            # mas a gente vai tratar isso no template:
            'tags': forms.CheckboxSelectMultiple(),
        }

class WorkoutDayExerciseForm(forms.ModelForm):
     class Meta:
         model = WorkoutDayExercise
         fields = ['exercise', 'order', 'custom_sets', 'custom_reps', 'rest_sec']
         widgets = {
            'exercise': forms.Select(),
            'order': forms.NumberInput(),
            'custom_sets': forms.NumberInput(),
            'custom_reps': forms.NumberInput(),
            'rest_sec': forms.NumberInput(),
            'exercise': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'custom_sets': forms.NumberInput(attrs={'class': 'form-control'}),
            'custom_reps': forms.NumberInput(attrs={'class': 'form-control'}),
            'rest_sec': forms.NumberInput(attrs={'class': 'form-control'}),
         }

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