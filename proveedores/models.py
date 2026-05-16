from django.db import models
from django.conf import settings

class Proveedor(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]

    ruc = models.CharField(max_length=11, unique=True, verbose_name="RUC")
    razon_social = models.CharField(max_length=200, verbose_name="Razón Social o Empresa")
    contacto = models.CharField(max_length=200, verbose_name="Representante / Contacto")
    telefono = models.CharField(max_length=50, verbose_name="Teléfono Celular")
    email = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', verbose_name="Estado")
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['razon_social']

    def __str__(self):
        return f"{self.ruc} - {self.razon_social}"
