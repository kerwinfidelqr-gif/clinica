from django.db import models
from django.conf import settings

class Paciente(models.Model):
    # Identificadores principales
    id_paciente = models.CharField(max_length=50, null=True, blank=True, verbose_name="ID Paciente")
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    DNI = models.CharField(max_length=10, verbose_name="DNI")
    
    # Datos Demográficos (Corregido el error de tipeo)
    lugar_nacimiento = models.CharField(max_length=100, verbose_name="Lugar de Nacimiento")
    edad = models.IntegerField(verbose_name="Edad")  # Cambiado a IntegerField para números
    sexo = models.CharField(max_length=50, verbose_name="Sexo")
    estado_civil = models.CharField(max_length=50, verbose_name="Estado Civil")
    
    # Datos de Contacto y Residencia
    domicilio_actual = models.CharField(max_length=150, verbose_name="Domicilio Actual")
    domicilio_procedencia = models.CharField(max_length=150, verbose_name="Domicilio de Procedencia")
    celular = models.CharField(max_length=20, verbose_name="Celular")
    ocupacion = models.CharField(max_length=100, verbose_name="Ocupación")
    
    # Datos Clínicos
    fecha_ingreso = models.DateField(verbose_name="Fecha de Ingreso") # Cambiado a DateField para usar calendarios
    estado = models.CharField(max_length=50,verbose_name="Estado")

    # Auditoría del Sistema (Basado en el tutorial)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Creado por")

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        # Opcional: Ordenar alfabéticamente por defecto
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - DNI: {self.DNI}"
    
    