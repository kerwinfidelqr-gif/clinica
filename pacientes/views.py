from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Paciente
from .forms import PacienteForm
from django.core.paginator import Paginator
from django.db import models
from usuarios.models import UsuarioRol

# 1. Vista de Listado
@login_required
def paciente_list(request): # Renombrado para mantener coherencia

    # CORRECCIÓN RBAC: Tu tabla usa 'usuario_id' y tu Rol usa 'pacientes'
    max_permission = UsuarioRol.objects.filter(usuario_id=request.user).aggregate(
        max_p=models.Max('rol__pacientes')
    )['max_p'] or 0

    if max_permission == 0:
        return redirect('dashboard')
    
    pacientes_list = Paciente.objects.all()

    # CORRECCIÓN SINTAXIS: request.GET debe ser en mayúsculas
    id_paciente = request.GET.get('id_paciente')
    nombre = request.GET.get('nombre')
    DNI = request.GET.get('DNI')
    estado_civil = request.GET.get('estado_civil') # El modelo Paciente no tiene 'estado', tiene 'estado_civil'

    # CORRECCIÓN FILTROS: Se debe usar doble guion bajo (__) y reasignar la variable
    if id_paciente:
        pacientes_list = pacientes_list.filter(id_paciente__icontains=id_paciente)
    if nombre:
        pacientes_list = pacientes_list.filter(nombre__icontains=nombre)
    if DNI:
        pacientes_list = pacientes_list.filter(DNI__icontains=DNI)
    if estado_civil:
        pacientes_list = pacientes_list.filter(estado_civil__icontains=estado_civil)

    # CORRECCIÓN VARIABLES: Se debe pasar pacientes_list, no material_list
    paginator = Paginator(pacientes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pacientes/pacientes_lista.html', {'page_obj': page_obj})


# 2. Vista de Creación
@login_required
def paciente_create(request):

    # CORRECCIÓN RBAC: Misma lógica de consulta a tu base de datos
    max_permission = UsuarioRol.objects.filter(usuario_id=request.user).aggregate(
        max_p=models.Max('rol__pacientes'))['max_p'] or 0

    if max_permission == 1:
        redirect('pacientes:paciente_list')
    if max_permission == 0:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            
            # CORRECCIÓN AUTENTICACIÓN: Django siempre usa request.user en las sesiones
            paciente.created_by = request.user 
            paciente.save()

            return redirect('pacientes:paciente_list')
    else:
        # CORRECCIÓN INDENTACIÓN: El else debe ir alineado con el 'if request.method'
        form = PacienteForm()

    return render(request, 'pacientes/paciente_form.html', {'form': form})