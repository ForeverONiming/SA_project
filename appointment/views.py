from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, AppointmentForm
from .models import Appointment, DOCTOR_LIST
import json

def home_view(request):
    return render(request, 'appointment/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'appointment/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'appointment/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def make_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, 'Appointment created!')
            return redirect('my_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'appointment/make_appointment.html', {'form': form})

@login_required
def make_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, 'Appointment created!')
            return redirect('my_appointments')
    else:
        form = AppointmentForm()
    # 傳 doctor_list_json 給前端
    context = {
        'form': form,
        'doctor_list_json': json.dumps(DOCTOR_LIST, ensure_ascii=False)
    }
    return render(request, 'appointment/make_appointment.html', context)
    
@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'appointment/my_appointments.html', {'appointments': appointments})