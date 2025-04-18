from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/add_task/', views.add_task, name='add_task'),
    path('task/<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/events/', views.task_events, name='task_events'),
    path('api/update-task-date/', views.update_task_date, name='update_task_date'),
    path('task/<int:pk>/complete/', views.complete_task, name='complete_task'),
    path('settings/', views.settings_view, name='settings'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),

]
