from django import forms
from .models import HistoriaClinica

class HistoriaClinicaForm(forms.ModelForm):
    # Campo extra que no se guarda en este modelo, solo sirve para buscar
    buscar_dni = forms.CharField(
        max_length=10, 
        required=False, 
        label="Buscar por DNI",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#233b6e]',
            'placeholder': 'Escriba el DNI y presione Enter...',
            'id': 'buscar_dni_input' # ID clave para JavaScript
        })
    )

    class Meta:
        model = HistoriaClinica
        fields = [
            'numero_historial', 'fecha_registro', 'especialidad', 'hora', 'grado_instruccion',
            'pa', 'pulso', 'temperatura', 'f_respiratoria', 'peso', 'talla', 'imc', 'alergias',
            'enfermedad_actual', 'examen_fisico'
        ]
        widgets = {
            # Los campos que se autocompletan los pondremos en el HTML directamente
            'numero_historial': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full'}),
            'especialidad': forms.Select(attrs={'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full'}),
            'grado_instruccion': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-lg px-3 py-2 w-full'}),
            # Funciones vitales
            'pa': forms.TextInput(attrs={'class': 'border-b border-gray-400 focus:outline-none w-full'}),
            'pulso': forms.TextInput(attrs={'class': 'border-b border-gray-400 focus:outline-none w-full'}),
            'temperatura': forms.TextInput(attrs={'class': 'border-b border-gray-400 focus:outline-none w-full'}),
            'f_respiratoria': forms.TextInput(attrs={'class': 'border-b border-gray-400 focus:outline-none w-full'}),
            'peso': forms.TextInput(attrs={'class': 'border-b border-gray-400 focus:outline-none w-full'}),
            'talla': forms.TextInput(attrs={'class': 'border-b border-gray-400 focus:outline-none w-full'}),
            'imc': forms.TextInput(attrs={'class': 'border-b border-gray-400 focus:outline-none w-full'}),
            'alergias': forms.TextInput(attrs={'class': 'border-b border-gray-400 focus:outline-none w-full'}),
            # Textos largos
            'enfermedad_actual': forms.Textarea(attrs={'rows': 4, 'class': 'w-full border border-gray-300 rounded-lg p-2'}),
            'examen_fisico': forms.Textarea(attrs={'rows': 4, 'class': 'w-full border border-gray-300 rounded-lg p-2'}),
        }