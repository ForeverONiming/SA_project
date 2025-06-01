
from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'time_slot', 'department', 'doctor', 'reason']
    search_fields = ['user__username', 'doctor', 'department']
    list_filter = ['department', 'date']