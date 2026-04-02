from django.urls import path
from . import views

app_name = 'pacientes'

urlpatterns = [
    path('', views.paciente_list, name='paciente_list'),
    path('create/', views.paciente_create, name='paciente_create'),
    path('edit/<int:pk>/', views.paciente_edit, name='paciente_edit'),
    path('delete/<int:pk>/', views.paciente_delete, name='paciente_delete'),
]