from django import forms
from django.contrib.auth.models import User

from core.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'text',)
