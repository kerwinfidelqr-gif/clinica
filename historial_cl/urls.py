from django.urls import path
from . import views

app_name = 'historial_cl'

urlpatterns = [
    # El dashboard ahora también es la lista principal
    path('', views.historial_dashboard, name='historial_dashboard'),
    
    # Rutas CRUD y PDF
    path('crear/', views.historial_create, name='historial_create'),
    path('editar/<int:pk>/', views.historial_edit, name='historial_edit'),
    path('eliminar/<int:pk>/', views.historial_delete, name='historial_delete'),
    path('pdf/<int:pk>/', views.generar_pdf, name='generar_pdf'),
    
    # API para autocompletar DNI
    path('api/buscar-paciente/', views.buscar_paciente_api, name='buscar_paciente_api'),
]