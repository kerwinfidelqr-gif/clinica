from django import forms
from .models import (
    IngresoHospitalario, HistoriaFiliacion, ExamenClinico,
    EvolucionMedica, EvolucionEnfermeria, TerapiaPrescripcion,
    InformeOperatorio, ConsentimientoInformado
)

# --- 1. Formulario Principal (Apertura de Carpeta) ---
class IngresoHospitalarioForm(forms.ModelForm):
    class Meta:
        model = IngresoHospitalario
        exclude = ['created_by'] # Se asignará automáticamente el usuario logueado
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_ingreso': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'numero_historia_clinica': forms.TextInput(attrs={'class': 'form-control'}),
            'cama': forms.TextInput(attrs={'class': 'form-control'}),
            'servicio': forms.TextInput(attrs={'class': 'form-control'}),
        }

# --- 2. Formularios de Detalle (Las hojas del expediente) ---
# OJO: Excluimos el campo 'ingreso' en todos, porque el sistema lo conectará automáticamente en segundo plano.

class HistoriaFiliacionForm(forms.ModelForm):
    class Meta:
        model = HistoriaFiliacion
        exclude = ['ingreso']

class ExamenClinicoForm(forms.ModelForm):
    class Meta:
        model = ExamenClinico
        exclude = ['ingreso']

class EvolucionMedicaForm(forms.ModelForm):
    class Meta:
        model = EvolucionMedica
        exclude = ['ingreso']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class EvolucionEnfermeriaForm(forms.ModelForm):
    class Meta:
        model = EvolucionEnfermeria
        exclude = ['ingreso']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class TerapiaPrescripcionForm(forms.ModelForm):
    class Meta:
        model = TerapiaPrescripcion
        exclude = ['ingreso']
        widgets = {
            'fecha_hora_prescripcion': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class InformeOperatorioForm(forms.ModelForm):
    class Meta:
        model = InformeOperatorio
        exclude = ['ingreso']
        widgets = {
            'h_inicio_op': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'h_fin_op': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class ConsentimientoInformadoForm(forms.ModelForm):
    class Meta:
        model = ConsentimientoInformado
        exclude = ['ingreso']