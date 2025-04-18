from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tasks import views as custom_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', custom_views.login_view, name='login'),  # Страница входа
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', custom_views.register, name='register'),  # Страница регистрации
    path('', include('tasks.urls')),  # Подключение маршрутов из tasks
]
