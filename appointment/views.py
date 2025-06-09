from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from .forms import RegisterForm, AppointmentForm, DoctorRegisterForm
from .models import Appointment, DOCTOR_LIST, DoctorProfile
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

def doctor_register(request):
    if request.method == 'POST':
        form = DoctorRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 註冊前先檢查這個 user 是否已有 DoctorProfile
            if DoctorProfile.objects.filter(user=user).exists():
                # 已經有，給錯誤訊息
                messages.error(request, "此帳號已是醫師，請勿重複註冊。")
                return redirect('doctor_register')
            # 沒有才新增
            DoctorProfile.objects.create(
                user=user,
                department=form.cleaned_data['department'],
                phone=form.cleaned_data['phone'],
            )
            messages.success(request, '註冊成功')
            return redirect('login')
    else:
        form = DoctorRegisterForm()
    return render(request, 'appointment/doctor_register.html', {'form': form})

def doctor_required(user):
    return user.is_superuser or hasattr(user, 'doctorprofile')

@login_required
@user_passes_test(doctor_required)
def doctor_dashboard(request):
    doctor = request.user.doctorprofile
    # 只顯示這位醫師的預約
    appointments = Appointment.objects.filter(doctor=doctor.user.username).order_by('-date', '-time_slot')
    return render(request, 'appointment/doctor_dashboard.html', {'doctor': doctor, 'appointments': appointments})

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
    # 查詢所有醫師，依科別分組
    doctors_by_dep = {}
    for d in DoctorProfile.objects.all():
        doctors_by_dep.setdefault(d.department, []).append(d.user.username)
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
    context = {
        'form': form,  # 用同一個 form 物件
        'doctor_list_json': json.dumps(doctors_by_dep, ensure_ascii=False),
    }
    return render(request, 'appointment/make_appointment.html', context)
    
@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-date', '-time_slot')
    return render(request, 'appointment/my_appointments.html', {'appointments': appointments})

@login_required
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == 'POST':
        appointment.delete()
        return redirect('my_appointments')
    return render(request, 'appointment/confirm_delete.html', {'appointment': appointment})

@login_required
def edit_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, '預約已成功修改！')
            return redirect('my_appointments')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointment/edit_appointment.html', {'form': form, 'appointment': appointment})

def doctor_stats(request):
    # 依醫師統計掛號數
    stats = (
        Appointment.objects.values('doctor', 'department')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    return render(request, 'appointment/doctor_stats.html', {'stats': stats})