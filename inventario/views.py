from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def inventario_dashboard(request):
    return render(request, 'inventario/lista_dashboard.html')