import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from xhtml2pdf import pisa 
from .models import HistoriaClinica
from .forms import HistoriaClinicaForm
from pacientes.models import Paciente
@login_required
def historial_dashboard(request):
    especialidades_principales = [
        {
            'nombre': 'Ginecoobstetricia', 
            'icono': 'fa-person-pregnant', 
            'color': 'bg-pink-500',
            'imagen': 'https://i.postimg.cc/13b5THV0/ginecoobstetricia.avif'
        },
        {
            'nombre': 'Pediatría', 
            'icono': 'fa-child', 
            'color': 'bg-orange-500',
            'imagen': 'https://i.postimg.cc/sgbD8cG9/pediatria.jpg'
        },
        {
            'nombre': 'Cirugía', 
            'icono': 'fa-scalpel-path', 
            'color': 'bg-blue-600',
            'imagen': 'https://i.postimg.cc/JzS4gqHx/cirugia.webp'
        },
        {
            'nombre': 'Medicina', 
            'icono': 'fa-stethoscope', 
            'color': 'bg-teal-500',
            'imagen': 'https://i.postimg.cc/rw7FbJRN/medicina.jpg'
        },
    ]

    historiales = HistoriaClinica.objects.all().order_by('-created_at')
    query = request.GET.get('q')
    if query:
        historiales = historiales.filter(paciente__DNI__icontains=query) | \
                      historiales.filter(paciente__nombre__icontains=query) | \
                      historiales.filter(numero_historial__icontains=query)

    paginator = Paginator(historiales, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'historial_cl/historial_dashboard.html', {
        'especialidades': especialidades_principales,
        'page_obj': page_obj,
        'query': query
    })
@login_required
def historial_create(request):
    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST)
        if form.is_valid():
            historial = form.save(commit=False)
            paciente_id = request.POST.get('paciente')
            historial.paciente = get_object_or_404(Paciente, id=paciente_id)
            historial.created_by = request.user
            historial.save()
            if 'print' in request.POST:
                return redirect('historial_cl:generar_pdf', pk=historial.pk)
            return redirect('historial_cl:historial_dashboard')
    else:
        form = HistoriaClinicaForm()
    return render(request, 'historial_cl/historial_form.html', {'form': form})
@login_required
def historial_edit(request, pk):
    historial = get_object_or_404(HistoriaClinica, pk=pk)
    paciente = historial.paciente
    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST, instance=historial)
        if form.is_valid():
            h = form.save(commit=False)
            paciente_id = request.POST.get('paciente')
            if paciente_id:
                h.paciente_id = paciente_id
            h.save()
            if 'print' in request.POST:
                return redirect('historial_cl:generar_pdf', pk=h.pk)
            return redirect('historial_cl:historial_dashboard')
    else:
        form = HistoriaClinicaForm(instance=historial, initial={'buscar_dni': paciente.DNI})
    return render(request, 'historial_cl/historial_form.html', {'form': form, 'historial': historial, 'paciente': paciente})

@login_required
def historial_delete(request, pk):
    historial = get_object_or_404(HistoriaClinica, pk=pk)
    historial.delete()
    return redirect('historial_cl:historial_dashboard')

@login_required
def generar_pdf(request, pk):
    historial = get_object_or_404(HistoriaClinica, pk=pk)
    template_path = 'historial_cl/historial_pdf_template.html'
    context = {'historial': historial, 'paciente': historial.paciente}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Historial_{historial.numero_historial}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
       return HttpResponse('Error al generar el PDF', status=500)
    return response

def buscar_paciente_api(request):
    dni = request.GET.get('dni', '')
    try:
        p = Paciente.objects.get(DNI=dni)
        return JsonResponse({
            'encontrado': True, 'id_interno': p.id, 'nombre_completo': p.nombre,
            'lugar_nacimiento': p.lugar_nacimiento, 'edad': p.edad, 'sexo': p.sexo,
            'domicilio_actual': p.domicilio_actual, 'domicilio_procedencia': p.domicilio_procedencia,
            'celular': p.celular, 'estado_civil': p.estado_civil, 'ocupacion': p.ocupacion
        })
    except Paciente.DoesNotExist:
        return JsonResponse({'encontrado': False, 'mensaje': 'Paciente no encontrado'})