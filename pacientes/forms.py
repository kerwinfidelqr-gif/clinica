from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'nombre', 'DNI', 'lugar_nacimiento', 'edad', 'sexo', 
            'estado_civil', 'domicilio_actual', 'domicilio_procedencia', 
            'celular', 'ocupacion', 'grado_instruccion', 'religion',
            'nombre_padre', 'nombre_madre', 'nombre_acompanante',
            'dni_acompanante', 'domicilio_acompanante'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#233b6e]'}),
            # Puedes agregar el resto de widgets con las mismas clases de Tailwind
        }