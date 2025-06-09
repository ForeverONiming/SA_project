from django.db import models
from django.contrib.auth.models import User

DEPARTMENT_CHOICES = [
    ('內科', '內科'),
    ('外科', '外科'),
    ('小兒科', '小兒科'),
    ('婦產科', '婦產科'),
    ('耳鼻喉科', '耳鼻喉科'),
    ('皮膚科', '皮膚科'),
    ('眼科', '眼科'),
]

# 這裡不用 DOCTOR_CHOICES，直接用 view 送所有醫師清單給前端
DOCTOR_LIST = {
    '內科':   ['王大明', '黃信義'],
    '外科':   ['李小華', '林惠玲'],
    '小兒科': ['陳志強', '張育慈'],
    '婦產科': ['陳美玉'],
    '耳鼻喉科': ['林子安'],
    '皮膚科': ['趙嘉芸'],
    '眼科':   ['沈建良'],
}

TIME_SLOT_CHOICES = [
    ('上午', '上午'),
    ('下午', '下午'),
    ('晚上', '晚上'),
]


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}（{self.department}）"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES, default='內科')
    doctor = models.CharField(max_length=10, default='王大明')
    date = models.DateField(default='2024-01-01')
    time_slot = models.CharField(max_length=4, choices=TIME_SLOT_CHOICES, default='上午')
    phone = models.CharField(max_length=20, default='')
    reason = models.CharField(max_length=200, default='')
    note = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} {self.time_slot}"
