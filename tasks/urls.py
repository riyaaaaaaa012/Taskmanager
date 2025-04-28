
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/',views.custom_logout,name='logout'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/edit/<int:task_id>/',views.task_edit, name='task_edit'),
    path('tasks/', views.task_list, name='task_list'),
    path('report/',views.task_report,name='task_report'),
]
