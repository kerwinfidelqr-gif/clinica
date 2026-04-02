from usuarios.models import UsuarioRol

def get_permissions(request):
    permissions = {
        'pacientes': 0,
        'proveedores': 0,
        'inventario': 0,
        'h_clinico': 0,
        'citas': 0,
    }
    roles = []

    if request.user.is_authenticated:
        # Filtramos los roles del usuario
        user_roles = UsuarioRol.objects.filter(usuario_id=request.user)
        roles = [ur.rol.nombre_rol for ur in user_roles]
        
        # Calculamos el permiso máximo
        for user_role in user_roles:
            rol = user_role.rol
            for module in permissions.keys():
                current_permission = getattr(rol, module, 0)
                if current_permission > permissions[module]:
                    permissions[module] = current_permission
                    
    return {'permissions': permissions, 'roles': roles}