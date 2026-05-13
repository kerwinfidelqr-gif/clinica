from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_proveedores(request):
    return render(request, 'proveedores/dashboard_proveedores.html')