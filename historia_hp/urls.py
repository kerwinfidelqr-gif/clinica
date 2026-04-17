from django.urls import path
from . import views

urlpatterns = [
    # Panel principal de hospitalización
    path('hospitalizados/', views.lista_ingresos, name='lista_ingresos'),
    
    # Crear la carpeta de ingreso
    path('hospitalizados/nuevo/', views.crear_ingreso, name='crear_ingreso'),
    
    # Ver el expediente completo de un paciente (usamos <int:pk> para identificar el ID)
    path('hospitalizados/expediente/<int:pk>/', views.detalle_ingreso, name='detalle_ingreso'),
    
    # Agregar hojas al expediente
    path('hospitalizados/expediente/<int:pk>/filiacion/', views.agregar_filiacion, name='agregar_filiacion'),
    path('hospitalizados/expediente/<int:pk>/evolucion/', views.agregar_evolucion, name='agregar_evolucion'),
    
    # Aquí puedes seguir agregando las rutas para el Informe Operatorio, Terapia, etc. siguiendo la misma lógica.
    path('hospitalizados/expediente/<int:pk>/examen/', views.agregar_examen, name='agregar_examen'),
    path('hospitalizados/expediente/<int:pk>/enfermeria/', views.agregar_enfermeria, name='agregar_enfermeria'),
    path('hospitalizados/expediente/<int:pk>/terapia/', views.agregar_terapia, name='agregar_terapia'),
    path('hospitalizados/expediente/<int:pk>/informe-op/', views.agregar_informe_op, name='agregar_informe_op'),
    path('hospitalizados/expediente/<int:pk>/consentimiento/', views.agregar_consentimiento, name='agregar_consentimiento'),
        # Rutas para imprimir PDFs
    path('hospitalizados/expediente/<int:pk>/imprimir-consentimiento/', views.imprimir_consentimiento, name='imprimir_consentimiento'),
    path('hospitalizados/expediente/<int:pk>/imprimir-filiacion/', views.imprimir_filiacion, name='imprimir_filiacion'),
    path('hospitalizados/expediente/<int:pk>/imprimir-examen/', views.imprimir_examen, name='imprimir_examen'),
]