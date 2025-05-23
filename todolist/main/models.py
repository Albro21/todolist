from django.db import models
from django.utils.timezone import now, localdate

from colorfield.fields import ColorField


class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('completed', 'Completed'),
    ]

    created_by = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True, related_name="projects")
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    color = ColorField(default='#FFFF00')
    company = models.ForeignKey('teams.Company', on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")
    client = models.CharField(max_length=50, blank=True)

    @property
    def total_tracked_time(self):
        total_seconds = int(sum(entry.duration.total_seconds() for entry in self.time_entries.all()))
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours}h {minutes}m {seconds}s"
    
    def __str__(self):
        return self.title


class Category(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="categories")
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    color = ColorField(default='#FFFF00')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


class Task(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="tasks")
    project = models.ForeignKey("main.Project", on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    categories = models.ManyToManyField(Category, blank=True, related_name="tasks")

    title = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    due_date = models.DateField()

    is_completed = models.BooleanField(default=False)
    is_high_priority = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['due_date']
    
    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        return self.due_date < localdate()

    def complete(self):
        self.is_completed = True
        self.completed_at = now().date()
        self.save()

    def toggle_priority(self):
        self.is_high_priority = not self.is_high_priority
        self.save()
