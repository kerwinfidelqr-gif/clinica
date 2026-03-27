from django import forms
from .models import Paciente

# CORRECCIÓN 1: La 'F' debe ser mayúscula (PacienteForm) para que coincida con tu views.py
class PacienteForm(forms.ModelForm):

    class Meta:
        model = Paciente
        
        # CORRECCIÓN 2: Agregué todos los campos que la recepcionista realmente necesita llenar.
        # (Nota: Omitimos 'created_by', 'created_at' y 'update_at' porque esos los llena el sistema automáticamente)
        fields = [
            'id_paciente', 'nombre', 'DNI', 'lugar_nacimiento', 
            'edad', 'sexo', 'estado_civil', 'domicilio_actual', 
            'domicilio_procedencia', 'celular', 'ocupacion', 'fecha_ingreso'
        ]

        # MEJORA PRO: Agregamos 'widgets' para inyectar clases CSS ('form-control') 
        # y ayudar a Celina con el diseño Frontend.
        widgets = {
            'id_paciente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: PAC-001'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres y Apellidos'}),
            'DNI': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de DNI'}),
            'lugar_nacimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'sexo': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_civil': forms.TextInput(attrs={'class': 'form-control'}),
            'domicilio_actual': forms.TextInput(attrs={'class': 'form-control'}),
            'domicilio_procedencia': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control'}),
            
            # EL TOQUE MAESTRO: 'type': 'date' obligará al navegador a mostrar un calendario interactivo.
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }