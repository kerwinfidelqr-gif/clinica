from django.db import models
from django.conf import settings

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('En Consultorio', 'En Consultorio'),
        ('Atendida', 'Atendida'),
        ('Cancelada', 'Cancelada'),
    ]

    paciente_nombre = models.CharField(max_length=200, verbose_name="Paciente (DNI o Nombre)")
    especialidad = models.CharField(max_length=100, verbose_name="Especialidad")
    medico_nombre = models.CharField(max_length=200, verbose_name="Médico")
    fecha = models.DateField(verbose_name="Fecha")
    hora = models.TimeField(verbose_name="Hora sugerida")
    motivo = models.TextField(blank=True, null=True, verbose_name="Motivo de consulta")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente', verbose_name="Estado")
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-fecha', '-hora']

    def __str__(self):
        return f"Cita: {self.paciente_nombre} con {self.medico_nombre} el {self.fecha} a las {self.hora}"
