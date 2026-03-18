from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache  # <-- Añade esto
from usuarios.models import UsuarioRol

@login_required
@never_cache
def dashboard_view(request):
    roles_usuarios = UsuarioRol.objects.filter(usuario_id=request.user)

    permissions = {
        'pacientes':0,
        'proveedores':0,
        'inventario':0,
        'h_clinico':0,
        'citas':0,
    }

    for rol_usuario in roles_usuarios:
        rol = rol_usuario.rol
        for module in permissions.keys():
            current_permission = getattr(rol,module)
            if current_permission > permissions[module]:
                permissions[module] = current_permission

    context = {
        'usuario': request.user,
        'permissions': permissions,
        'roles': [ur.rol.nombre_rol for ur in roles_usuarios],
    }

    return render(request, 'core/dashboard.html', context)