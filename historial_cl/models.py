from django.db import models
from django.conf import settings
from django.utils import timezone
from pacientes.models import Paciente

class HistoriaClinica(models.Model):
    # Relación OBLIGATORIA
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='historias_clinicas', verbose_name="Paciente")
    
    # ENCABEZADO (OBLIGATORIOS)
    numero_historial = models.CharField(max_length=50, verbose_name="N° de Historia Clínica")
    
    ESPECIALIDADES_CHOICES = [
        ('Colposcopia', 'Colposcopia'), ('Crioterapia', 'Crioterapia'),
        ('Medicina Pediátrica', 'Medicina Pediátrica'), ('Consulta del Niño Sano', 'Consulta del Niño Sano'),
        ('Cirugía General', 'Cirugía General'), ('Neurocirugía', 'Neurocirugía'), 
        ('Cirugía Plástica', 'Cirugía Plástica'), ('Cirugía Maxilofacial', 'Cirugía Maxilofacial'),
        ('Traumatología', 'Traumatología'), ('Urología', 'Urología'), ('Cirugía de cabeza y cuello', 'Cirugía de cabeza y cuello'),
        ('Otorrinolaringología', 'Otorrinolaringología'), ('Neurología', 'Neurología'), 
        ('Cardiología', 'Cardiología'), ('Endocrinología', 'Endocrinología'), 
        ('Gastroenterología', 'Gastroenterología'), ('Dermatología', 'Dermatología'), 
        ('Medicina Física y Rehabilitación', 'Medicina Física y Rehabilitación'), 
        ('Oncología Clínica', 'Oncología Clínica'), ('Psicología', 'Psicología'),
    ]
    especialidad = models.CharField(max_length=100, choices=ESPECIALIDADES_CHOICES, verbose_name="Especialidad")
    
    # --- FECHA DE REGISTRO ---
    fecha_registro = models.DateField(verbose_name="Fecha de Registro", blank=True, null=True)
    
    # --- CAMPOS OPCIONALES (Agregamos blank=True, null=True) ---
    hora = models.TimeField(verbose_name="Hora", blank=True, null=True)
    grado_instruccion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Grado de Instrucción")

    # FUNCIONES VITALES (Ya eran opcionales)
    pa = models.CharField(max_length=20, blank=True, null=True, verbose_name="P/A")
    pulso = models.CharField(max_length=20, blank=True, null=True, verbose_name="Pulso")
    temperatura = models.CharField(max_length=20, blank=True, null=True, verbose_name="Temperatura")
    f_respiratoria = models.CharField(max_length=20, blank=True, null=True, verbose_name="F/Respiratoria")
    peso = models.CharField(max_length=20, blank=True, null=True, verbose_name="Peso")
    talla = models.CharField(max_length=20, blank=True, null=True, verbose_name="Talla")
    imc = models.CharField(max_length=20, blank=True, null=True, verbose_name="IMC")
    alergias = models.CharField(max_length=200, blank=True, null=True, verbose_name="Alergias")

    # TEXTOS MÉDICOS (Ahora son opcionales)
    enfermedad_actual = models.TextField(verbose_name="Enfermedad Actual", blank=True, null=True)
    examen_fisico = models.TextField(verbose_name="Examen Físico", blank=True, null=True)

    # AUDITORÍA
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Historia Clínica'
        verbose_name_plural = 'Historias Clínicas'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.fecha_registro:
            from datetime import datetime, time
            if self.created_at:
                self.created_at = datetime.combine(self.fecha_registro, self.created_at.time())
            else:
                self.created_at = datetime.combine(self.fecha_registro, time.min)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Historial {self.numero_historial} - {self.paciente.nombre}"


        