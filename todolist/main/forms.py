from django import forms
from .models import Project, Category, Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'status', 'color', 'client']
    
    status = forms.CharField(required=False)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'description', 'color']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'text', 'project', 'categories', 'due_date', 'is_high_priority']
