from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_cita, name='dashboard_cita'),
]
