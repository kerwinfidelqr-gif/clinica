from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol, UsuarioRol

@admin.register(Usuario)
class CustomUsuarioAdmin(UserAdmin):
    # Usamos los nombres reales de los campos del modelo (en inglés por AbstractUser)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    
    # Corregimos los filtros usando también los nombres reales
    list_filter = ('is_staff', 'is_active', 'date_joined')
    
    # Búsqueda por los campos reales
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Configuración de nombres para que se vean en español en la columna (Opcional)
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['username'].label = 'Nombre de Usuario'
        return form

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    # CORRECCIÓN IMPORTANTE:
    # 1. 'historial clinico' (con espacio) da error -> Cambiar a 'h_clinico' (nombre en el modelo)
    # 2. Asegurarse que los nombres coincidan con models.py
    list_display = ('nombre_rol', 'pacientes', 'proveedores', 'inventario', 'h_clinico', 'citas')
    
    list_filter = ('pacientes', 'proveedores', 'inventario', 'h_clinico', 'citas')
    
    search_fields = ('nombre_rol',)

@admin.register(UsuarioRol)
class RolUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario_id', 'rol')
    list_filter = ('rol',)
    # Corregido para buscar por los campos relacionados correctos
    search_fields = ('usuario_id__username', 'rol__nombre_rol')