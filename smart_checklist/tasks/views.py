from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task
from django.http import JsonResponse
from .forms import TaskForm, ProjectForm
from django.utils import timezone
from django.contrib.auth.forms import PasswordChangeForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import UserSettingsForm, CustomPasswordChangeForm


@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    selected_project = None
    tasks = None

    # Обработка формы добавления проекта
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_list')
    else:
        project_form = ProjectForm()

    # Получаем ID выбранного проекта
    project_id = request.GET.get('project')
    if project_id:
        selected_project = Project.objects.filter(id=project_id, user=request.user).first()
        if selected_project:
            tasks = selected_project.tasks.all().order_by('due_date')

    context = {
        'projects': projects,
        'project_form': project_form,
        'selected_project': selected_project,
        'tasks': tasks,
    }

    return render(request, 'tasks/project_list.html', context)


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all().order_by('due_date')
    return render(request, 'tasks/project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def add_task(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', pk=pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'project': project})

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'task': task})

@login_required
def calendar_view(request):
    return render(request, 'tasks/calendar.html')

@login_required
def task_events(request):
    # Фильтруем задачи по текущему пользователю
    tasks = Task.objects.filter(project__user=request.user)
    events = []
    for task in tasks:
        events.append({
            'id': task.id,
            'title': f"{task.title} ({task.project.name})",
            'start': str(task.due_date),
            'color': {
                'low': '#28a745',
                'medium': '#ffc107',
                'high': '#dc3545',
            }.get(task.priority, '#007bff'),
            'borderColor': '#000' if task.is_overdue() else None,
        })
    return JsonResponse(events, safe=False)

@csrf_exempt
def update_task_date(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('id')
        new_date = data.get('new_date')
        try:
            task = Task.objects.get(pk=task_id)
            task.due_date = new_date
            task.save()
            return HttpResponse("OK")
        except Task.DoesNotExist:
            return HttpResponseBadRequest("Task not found")
    return HttpResponseBadRequest("Invalid request")

@login_required
@csrf_exempt
def complete_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        task.delete()  # Удаляем задачу
        return redirect('project_list')
    return JsonResponse({'success': False}, status=400)



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'tasks/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('calendar')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('calendar')
    else:
        form = AuthenticationForm()

    return render(request, 'tasks/login.html', {'form': form})


@login_required
def settings_view(request):
    if request.method == 'POST':
        if request.POST.get('form_type') == 'user_form':
            user_form = UserSettingsForm(request.POST, instance=request.user)
            password_form = CustomPasswordChangeForm(user=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Имя пользователя обновлено.')
        else:
            user_form = UserSettingsForm(instance=request.user)
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль успешно обновлён.')
    else:
        user_form = UserSettingsForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'tasks/settings.html', {
        'user_form': user_form,
        'password_form': password_form
    })

def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    project.delete()
    return redirect('project_list')