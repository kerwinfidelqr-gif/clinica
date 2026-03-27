from django.urls import path
from . import views

# Este es el "Apellido" de tus rutas (Namespace)
app_name = 'pacientes'

urlpatterns = [
    # Lo dejé en singular ('paciente_list') para que coincida exactamente con el nombre de tu vista
    path('', views.paciente_list, name='paciente_list'),
    
    # ¡CORRECCIÓN! Tenías 'pacinete_create' (con la 'n' y la 'e' invertidas)
    path('create/', views.paciente_create, name='paciente_create'),
]