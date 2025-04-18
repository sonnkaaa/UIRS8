from django import forms
from .models import Task, Project
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control fixed-width'}),
            'description': forms.Textarea(attrs={'class': 'form-control fixed-width', 'rows': 3, 'style': 'resize: none;'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control fixed-width'}),
            'priority': forms.Select(attrs={'class': 'form-select fixed-width'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control'
        })


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })