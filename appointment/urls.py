
from django.urls import path
from . import views

urlpatterns = [
    path('doctor_register/', views.doctor_register, name='doctor_register'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'), 
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('make/', views.make_appointment, name='make_appointment'),
    path('my/', views.my_appointments, name='my_appointments'),
    path('delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
    path('edit/<int:pk>/', views.edit_appointment, name='edit_appointment'),
    path('my/edit/<int:pk>/', views.edit_appointment, name='edit_appointment'), 
    path('my/delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
    path('doctor_stats/', views.doctor_stats, name='doctor_stats'),
]
