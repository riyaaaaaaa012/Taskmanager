# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import Task
from .forms import TaskForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.set_password(form.cleaned_data['password'])  
            user.save()  
            login(request, user)  
            return redirect('login')  
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def task_create(request):

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_create.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.all()

    # Filtering by status
    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)

    # Filtering by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        tasks = tasks.filter(due_date__range=[start_date, end_date])

    
   
    return render(request, 'task_list.html', {'tasks': tasks})
@login_required
def task_report(request):
    # Get all tasks with complete details
    tasks = Task.objects.all().order_by('-due_date')
    
    # Summary statistics (kept for reference)
    completed_count = Task.objects.filter(status='completed').count()
    pending_count = Task.objects.exclude(status='completed').count()

    context = {
        'tasks': tasks,  # Full task objects
        'completed_count': completed_count,
        'pending_count': pending_count,
        'total_count': tasks.count()  # Optional
    }
    return render(request, 'task_report.html', context)

@login_required
def task_edit(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_edit.html', {'form': form})

@require_http_methods(['GET', 'POST'])
def custom_logout(request):
    logout(request)
    return redirect('login')
