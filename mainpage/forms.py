from django import forms
from mainpage.models import Task, Profile


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'text',)
