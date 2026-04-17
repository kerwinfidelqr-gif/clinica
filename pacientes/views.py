import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Paciente
from .forms import PacienteForm

@login_required
def paciente_list(request):
    pacientes_list = Paciente.objects.all().order_by('-id')
    nombre = request.GET.get('nombre')
    dni_filter = request.GET.get('DNI')  # Evitamos usar 'DNI' en mayúscula como variable
    if nombre:
        pacientes_list = pacientes_list.filter(nombre__icontains=nombre)
    if dni_filter:
        pacientes_list = pacientes_list.filter(DNI__icontains=dni_filter)

    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="pacientes.csv"'
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response, delimiter=';')
        writer.writerow(['ID', 'Nombre', 'DNI', 'Edad', 'Celular'])
        for p in pacientes_list:
            writer.writerow([p.id_paciente, p.nombre, p.DNI, p.edad, p.celular])
        return response
    paginator = Paginator(pacientes_list, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'pacientes/pacientes_lista.html', {'page_obj': page_obj})

@login_required
def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.created_by = request.user
            paciente.save()
            return redirect('pacientes:paciente_list')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/paciente_form.html', {'form': form})

@login_required
def paciente_edit(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('pacientes:paciente_list')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'pacientes/paciente_form.html', {'form': form, 'paciente': paciente})

@login_required
def paciente_delete(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    paciente.delete()
    return redirect('pacientes:paciente_list')