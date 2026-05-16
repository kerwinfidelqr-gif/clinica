from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Cita
from datetime import date

@login_required
def dashboard_cita(request):
    if request.method == 'POST':
        paciente_nombre = request.POST.get('paciente_nombre')
        especialidad = request.POST.get('especialidad')
        medico_nombre = request.POST.get('medico_nombre')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        motivo = request.POST.get('motivo')

        Cita.objects.create(
            paciente_nombre=paciente_nombre,
            especialidad=especialidad,
            medico_nombre=medico_nombre,
            fecha=fecha,
            hora=hora,
            motivo=motivo,
            created_by=request.user
        )
        return redirect('dashboard_cita')

    hoy = date.today()
    citas_hoy = Cita.objects.filter(fecha=hoy).exclude(estado='Cancelada').order_by('hora')
    citas_cal = Cita.objects.exclude(estado='Cancelada')

    context = {
        'citas_hoy': citas_hoy,
        'citas_cal': citas_cal,
    }
    return render(request, 'citas/dashboard_cita.html', context)
