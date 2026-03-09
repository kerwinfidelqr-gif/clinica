from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    usuario_id = models.AutoField(primary_key=True)
    nom_usuario = models.CharField(max_length=100, unique=True) # Agregué unique=True por seguridad
    password = models.CharField(max_length=100)

    # CORREGIDO: Django necesita que esta variable se llame exactamente así:
    USERNAME_FIELD = 'nom_usuario'
    
    # Campos requeridos al crear superusuario (aparte de nom_usuario y password)
    REQUIRED_FIELDS = ['username', 'email']

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Rol(models.Model):
    PERMISSION_CHOICES = [
        (0,'Sin acceso'),
        (1,'Vista'),
        (2,'Crear y modificar'),
    ]

    nombre_rol = models.CharField(max_length=100, primary_key=True)

    pacientes = models.IntegerField(choices=PERMISSION_CHOICES, default=0)
    proveedores = models.IntegerField(choices=PERMISSION_CHOICES, default=0)
    inventario = models.IntegerField(choices=PERMISSION_CHOICES, default=0)
    h_clinico = models.IntegerField(choices=PERMISSION_CHOICES, default=0)
    citas = models.IntegerField(choices=PERMISSION_CHOICES, default=0)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        
    def __str__(self):
        return self.nombre_rol
        
class UsuarioRol(models.Model):
    # Nota: Es mejor llamar al campo 'usuario' en lugar de 'usuario_id' para evitar 'usuario_id_id'
    # pero lo dejo así para no romper tu código existente.
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    class Meta:
        db_table = 'usuario_roles'
        verbose_name = 'Usuario Rol'
        verbose_name_plural = 'Usuario Roles'
        unique_together = ('usuario_id', 'rol')
    
    def __str__(self):
        # Usamos nom_usuario ya que es tu campo principal
        return f"{self.usuario_id.nom_usuario} - {self.rol.nombre_rol}"