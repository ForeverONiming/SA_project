from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Appointment, DoctorProfile
from .models import Appointment, DEPARTMENT_CHOICES, DOCTOR_LIST, TIME_SLOT_CHOICES

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DoctorRegisterForm(UserCreationForm):
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, label="科別", widget=forms.Select(attrs={'class': 'form-select'}))
    phone = forms.CharField(max_length=20, label="聯絡電話", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit)
        DoctorProfile.objects.create(
            user=user,
            department=self.cleaned_data['department'],
            phone=self.cleaned_data['phone']
        )
        return user

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['department', 'doctor', 'date', 'time_slot', 'phone', 'reason', 'note']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_slot': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0912-345678'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
        labels = {
            'department': '科別',
            'doctor': '醫師',
            'date': '日期',
            'time_slot': '時段',
            'phone': '聯絡電話',
            'reason': '掛號原因',
            'note': '備註（可選）',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].choices = [('', '請先選擇科別')]