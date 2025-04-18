from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'В работе'),
        ('done', 'Завершено'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    description = models.TextField(blank=True)

    def is_overdue(self):
        return self.status == 'todo' and self.due_date < timezone.now().date()

    def __str__(self):
        return self.title
