from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# IMPORTAMOS TODOS LOS MODELOS
from .models import (
    IngresoHospitalario, EvolucionMedica, HistoriaFiliacion,
    ExamenClinico, EvolucionEnfermeria, TerapiaPrescripcion,
    InformeOperatorio, ConsentimientoInformado
)

# IMPORTAMOS TODOS LOS FORMULARIOS
from .forms import (
    IngresoHospitalarioForm, EvolucionMedicaForm, HistoriaFiliacionForm,
    ExamenClinicoForm, EvolucionEnfermeriaForm, TerapiaPrescripcionForm,
    InformeOperatorioForm, ConsentimientoInformadoForm
)

# --- 1. PANEL PRINCIPAL ---
@login_required
def lista_ingresos(request):
    # Mostramos todos los pacientes internados, ordenados por los más recientes
    ingresos = IngresoHospitalario.objects.all().order_by('-fecha_ingreso', '-hora_ingreso')
    return render(request, 'historia_hp/lista_ingresos.html', {'ingresos': ingresos})

# --- 2. CREAR LA CARPETA (INGRESO) ---
@login_required
def crear_ingreso(request):
    if request.method == 'POST':
        form = IngresoHospitalarioForm(request.POST)
        if form.is_valid():
            # commit=False pausa el guardado para que podamos inyectar datos
            ingreso = form.save(commit=False)
            ingreso.created_by = request.user # Registramos qué doctor hizo el ingreso
            ingreso.save()
            messages.success(request, "Ingreso hospitalario creado exitosamente.")
            return redirect('detalle_ingreso', pk=ingreso.pk)
    else:
        form = IngresoHospitalarioForm()
    
    return render(request, 'historia_hp/form_basico.html', {'form': form, 'titulo': 'Nuevo Ingreso Hospitalario'})

# --- 3. EL TABLERO DEL PACIENTE (EXPEDIENTE) ---
@login_required
def detalle_ingreso(request, pk):
    ingreso = get_object_or_404(IngresoHospitalario, pk=pk)
    
    context = {
        'ingreso': ingreso,
        # Verificación de documentos únicos (OneToOne)
        'tiene_filiacion': hasattr(ingreso, 'historiafiliacion'), 
        'tiene_examen': hasattr(ingreso, 'examenclinico'),
        'tiene_informe': hasattr(ingreso, 'informeoperatorio'),
        'tiene_consentimiento': hasattr(ingreso, 'consentimientoinformado'),
        
        # Listas de registros múltiples (ForeignKey)
        'evoluciones': ingreso.evoluciones_medicas.all().order_by('-fecha_hora'),
        'notas_enfermeria': ingreso.notas_enfermeria.all().order_by('-fecha_hora'),
        'terapias': ingreso.terapias.all().order_by('-fecha_hora_prescripcion'),
    }
    return render(request, 'historia_hp/detalle_ingreso.html', context)
# --- 4. AGREGAR HOJAS AL EXPEDIENTE ---

@login_required
def agregar_filiacion(request, pk):
    ingreso = get_object_or_404(IngresoHospitalario, pk=pk)
    if request.method == 'POST':
        form = HistoriaFiliacionForm(request.POST)
        if form.is_valid():
            filiacion = form.save(commit=False)
            filiacion.ingreso = ingreso # ¡El truco! Conectamos la hoja a la carpeta
            filiacion.save()
            messages.success(request, "Filiación guardada correctamente.")
            return redirect('detalle_ingreso', pk=ingreso.pk)
    else:
        form = HistoriaFiliacionForm()
    return render(request, 'historia_hp/form_basico.html', {'form': form, 'titulo': 'Agregar Historia de Filiación', 'ingreso': ingreso})

@login_required
def agregar_evolucion(request, pk):
    ingreso = get_object_or_404(IngresoHospitalario, pk=pk)
    if request.method == 'POST':
        form = EvolucionMedicaForm(request.POST)
        if form.is_valid():
            evolucion = form.save(commit=False)
            evolucion.ingreso = ingreso # Conectamos la hoja a la carpeta
            evolucion.save()
            messages.success(request, "Evolución médica agregada al expediente.")
            return redirect('detalle_ingreso', pk=ingreso.pk)
    else:
        form = EvolucionMedicaForm()
    return render(request, 'historia_hp/form_basico.html', {'form': form, 'titulo': 'Nueva Evolución Médica', 'ingreso': ingreso})

# --- LAS NUEVAS HOJAS MÉDICAS ---

@login_required
def agregar_examen(request, pk):
    ingreso = get_object_or_404(IngresoHospitalario, pk=pk)
    if request.method == 'POST':
        form = ExamenClinicoForm(request.POST)
        if form.is_valid():
            examen = form.save(commit=False)
            examen.ingreso = ingreso
            examen.save()
            messages.success(request, "Examen Clínico guardado.")
            return redirect('detalle_ingreso', pk=ingreso.pk)
    else:
        form = ExamenClinicoForm()
    return render(request, 'historia_hp/form_basico.html', {'form': form, 'titulo': 'Examen Clínico Inicial', 'ingreso': ingreso})

@login_required
def agregar_enfermeria(request, pk):
    ingreso = get_object_or_404(IngresoHospitalario, pk=pk)
    if request.method == 'POST':
        form = EvolucionEnfermeriaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.ingreso = ingreso
            nota.save()
            messages.success(request, "Nota de enfermería agregada.")
            return redirect('detalle_ingreso', pk=ingreso.pk)
    else:
        form = EvolucionEnfermeriaForm()
    return render(request, 'historia_hp/form_basico.html', {'form': form, 'titulo': 'Nueva Nota de Enfermería', 'ingreso': ingreso})

@login_required
def agregar_terapia(request, pk):
    ingreso = get_object_or_404(IngresoHospitalario, pk=pk)
    if request.method == 'POST':
        form = TerapiaPrescripcionForm(request.POST)
        if form.is_valid():
            terapia = form.save(commit=False)
            terapia.ingreso = ingreso
            terapia.save()
            messages.success(request, "Terapia prescrita correctamente.")
            return redirect('detalle_ingreso', pk=ingreso.pk)
    else:
        form = TerapiaPrescripcionForm()
    return render(request, 'historia_hp/form_basico.html', {'form': form, 'titulo': 'Prescribir Nueva Terapia', 'ingreso': ingreso})

@login_required
def agregar_informe_op(request, pk):
    ingreso = get_object_or_404(IngresoHospitalario, pk=pk)
    if request.method == 'POST':
        form = InformeOperatorioForm(request.POST)
        if form.is_valid():
            informe = form.save(commit=False)
            informe.ingreso = ingreso
            informe.save()
            messages.success(request, "Informe operatorio guardado.")
            return redirect('detalle_ingreso', pk=ingreso.pk)
    else:
        form = InformeOperatorioForm()
    return render(request, 'historia_hp/form_basico.html', {'form': form, 'titulo': 'Informe Operatorio', 'ingreso': ingreso})

@login_required
def agregar_consentimiento(request, pk):
    ingreso = get_object_or_404(IngresoHospitalario, pk=pk)
    if request.method == 'POST':
        form = ConsentimientoInformadoForm(request.POST)
        if form.is_valid():
            consentimiento = form.save(commit=False)
            consentimiento.ingreso = ingreso
            consentimiento.save()
            messages.success(request, "Consentimiento Informado registrado.")
            return redirect('detalle_ingreso', pk=ingreso.pk)
    else:
        form = ConsentimientoInformadoForm()
    return render(request, 'historia_hp/form_basico.html', {'form': form, 'titulo': 'Consentimiento Informado', 'ingreso': ingreso})


# --- IMPORTACIONES NUEVAS PARA PDF ---
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# --- FUNCIÓN PARA GENERAR EL PDF DEL CONSENTIMIENTO ---
@login_required
def imprimir_consentimiento(request, pk):
    # Aquí sí funcionará get_object_or_404 porque ya está importado arriba en este archivo
    ingreso = get_object_or_404(IngresoHospitalario, pk=pk)
    
    # Validamos que el documento exista antes de imprimir
    if not hasattr(ingreso, 'consentimientoinformado'):
        messages.error(request, "Aún no se ha llenado el Consentimiento Informado.")
        return redirect('detalle_ingreso', pk=ingreso.pk)

    # Definimos la plantilla HTML y los datos que le enviaremos
    template_path = 'historia_hp/pdfs/consentimiento_pdf.html'
    context = {
        'ingreso': ingreso,
        'consentimiento': ingreso.consentimientoinformado
    }
    
    # Preparamos la respuesta HTTP para que el navegador sepa que es un PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Consentimiento_{ingreso.numero_historia_clinica}.pdf"'
    
    # Renderizamos el HTML con los datos
    template = get_template(template_path)
    html = template.render(context)

    # Creamos el PDF mágico
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Si hay un error, mostramos el mensaje
    if pisa_status.err:
        return HttpResponse(f'Tuvimos algunos errores <pre>{html}</pre>')
    return response

    # --- IMPRESIÓN DE HISTORIA DE FILIACIÓN ---
@login_required
def imprimir_filiacion(request, pk):
    ingreso = get_object_or_404(IngresoHospitalario, pk=pk)
    if not hasattr(ingreso, 'historiafiliacion'):
        messages.error(request, "Aún no se ha llenado la Historia de Filiación.")
        return redirect('detalle_ingreso', pk=ingreso.pk)

    template_path = 'historia_hp/pdfs/filiacion_pdf.html'
    context = {'ingreso': ingreso, 'filiacion': ingreso.historiafiliacion}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Filiacion_{ingreso.numero_historia_clinica}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    return response

# --- IMPRESIÓN DE EXAMEN CLÍNICO ---
@login_required
def imprimir_examen(request, pk):
    ingreso = get_object_or_404(IngresoHospitalario, pk=pk)
    if not hasattr(ingreso, 'examenclinico'):
        messages.error(request, "Aún no se ha registrado el Examen Clínico.")
        return redirect('detalle_ingreso', pk=ingreso.pk)

    template_path = 'historia_hp/pdfs/examen_pdf.html'
    context = {'ingreso': ingreso, 'examen': ingreso.examenclinico}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Examen_{ingreso.numero_historia_clinica}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    return response