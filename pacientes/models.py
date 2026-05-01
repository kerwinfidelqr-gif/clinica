from django.db import models
from django.conf import settings

class Paciente(models.Model):
    # El ID ahora es único y no editable manualmente
    id_paciente = models.CharField(max_length=50, null=True, blank=True, unique=True, editable=False, verbose_name="ID Paciente")
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    DNI = models.CharField(max_length=10, verbose_name="DNI")
    lugar_nacimiento = models.CharField(max_length=100, verbose_name="Lugar de Nacimiento")
    edad = models.IntegerField(verbose_name="Edad")
    sexo = models.CharField(max_length=50, verbose_name="Sexo")
    estado_civil = models.CharField(max_length=50, verbose_name="Estado Civil")
    domicilio_actual = models.CharField(max_length=150, verbose_name="Domicilio Actual")
    domicilio_procedencia = models.CharField(max_length=150, verbose_name="Domicilio de Procedencia")
    celular = models.CharField(max_length=20, verbose_name="Celular")
    ocupacion = models.CharField(max_length=100, verbose_name="Ocupación")
    fecha_ingreso = models.DateField(verbose_name="Fecha de Ingreso", auto_now_add=True, null=True)
    estado = models.CharField(max_length=50, verbose_name="Estado")
    
    # Nuevos campos del formulario HTML
    grado_instruccion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Grado de Instrucción")
    religion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Religión")
    nombre_padre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre del Padre")
    nombre_madre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre de la Madre")
    nombre_acompanante = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre del Acompañante")
    dni_acompanante = models.CharField(max_length=15, blank=True, null=True, verbose_name="DNI Acompañante")
    domicilio_acompanante = models.CharField(max_length=150, blank=True, null=True, verbose_name="Domicilio Acompañante")
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.id_paciente:
            ultimo = Paciente.objects.all().order_by('id').last()
            if ultimo and ultimo.id_paciente:
                try:
                    num = int(ultimo.id_paciente.split('-')[1]) + 1
                except:
                    num = 1
            else:
                num = 1
            self.id_paciente = f'PAC-{num:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_paciente} - {self.nombre}"