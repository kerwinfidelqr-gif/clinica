from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def citas_dashboard(request):
    return render(request, 'dashboard_cita.html')