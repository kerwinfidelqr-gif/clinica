from django.db import models
from django.conf import settings
from pacientes.models import Paciente  # Asumiendo que así se llama tu modelo de pacientes

# --- MODELO MAESTRO: LA CARPETA PRINCIPAL DEL INTERNAMIENTO ---
class IngresoHospitalario(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='ingresos_hospitalarios')
    numero_historia_clinica = models.CharField(max_length=50, unique=True)
    cama = models.CharField(max_length=20)
    servicio = models.CharField(max_length=100)
    fecha_ingreso = models.DateField()
    hora_ingreso = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Ingreso {self.numero_historia_clinica} - {self.paciente.nombre}"

# --- MODELOS DE DETALLE: LAS HOJAS DEL EXPEDIENTE ---

class HistoriaFiliacion(models.Model):
    ingreso = models.OneToOneField(IngresoHospitalario, on_delete=models.CASCADE)
    raza = models.CharField(max_length=50, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    nombre_padre = models.CharField(max_length=150, blank=True)
    nombre_madre = models.CharField(max_length=150, blank=True)
    acompanante_nombre = models.CharField(max_length=150, blank=True)
    acompanante_dni = models.CharField(max_length=15, blank=True)
    acompanante_domicilio = models.CharField(max_length=255, blank=True)
    enfermedad_actual = models.TextField(blank=True)

class ExamenClinico(models.Model):
    ingreso = models.OneToOneField(IngresoHospitalario, on_delete=models.CASCADE)
    # Funciones Vitales Iniciales
    temperatura = models.CharField(max_length=10)
    fc = models.CharField(max_length=10) # Frecuencia Cardiaca
    fr = models.CharField(max_length=10) # Frecuencia Respiratoria
    pa = models.CharField(max_length=20) # Presión Arterial
    peso = models.CharField(max_length=10)
    talla = models.CharField(max_length=10)
    imc = models.CharField(max_length=10)
    # Examen Físico detallado
    examen_general = models.TextField(help_text="Estado de conciencia, nutrición, piel, etc.")
    examen_regional = models.TextField(help_text="Cabeza, Cuello, Tórax, Abdomen, etc.")

class EvolucionMedica(models.Model):
    ingreso = models.ForeignKey(IngresoHospitalario, on_delete=models.CASCADE, related_name='evoluciones_medicas')
    fecha_hora = models.DateTimeField()
    apreciacion_subjetiva = models.TextField()
    apreciacion_objetiva = models.TextField()
    tratamiento_plan_trabajo = models.TextField()
    firma_medico = models.CharField(max_length=150)

class EvolucionEnfermeria(models.Model):
    ingreso = models.ForeignKey(IngresoHospitalario, on_delete=models.CASCADE, related_name='notas_enfermeria')
    fecha_hora = models.DateTimeField()
    anotacion = models.TextField()
    ingresos_liquidos = models.CharField(max_length=50, blank=True)
    egresos_liquidos = models.CharField(max_length=50, blank=True)

class TerapiaPrescripcion(models.Model):
    ingreso = models.ForeignKey(IngresoHospitalario, on_delete=models.CASCADE, related_name='terapias')
    fecha_hora_prescripcion = models.DateTimeField()
    terapia = models.TextField()
    via_administracion = models.CharField(max_length=100)
    horario = models.CharField(max_length=100)

class InformeOperatorio(models.Model):
    ingreso = models.OneToOneField(IngresoHospitalario, on_delete=models.CASCADE)
    codigo_operacion = models.CharField(max_length=50)
    diagnostico_pre_op = models.TextField()
    diagnostico_post_op = models.TextField()
    operacion_realizada = models.TextField()
    cirujano = models.CharField(max_length=150)
    anestesiologo = models.CharField(max_length=150)
    tecnica_anestesica = models.CharField(max_length=150)
    h_inicio_op = models.TimeField()
    h_fin_op = models.TimeField()
    descripcion_operacion = models.TextField()
    tipo_herida = models.CharField(max_length=5, choices=[('A','A'), ('B','B'), ('C','C'), ('D','D')])

class ConsentimientoInformado(models.Model):
    ingreso = models.OneToOneField(IngresoHospitalario, on_delete=models.CASCADE)
    medico_responsable = models.CharField(max_length=150)
    especialidad = models.CharField(max_length=100)
    riesgos_procedimiento = models.TextField()
    consecuencias_no_realizar = models.TextField()
    firma_paciente_confirmada = models.BooleanField(default=False)