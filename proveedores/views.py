from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Proveedor

@login_required
def dashboard_proveedores(request):
    if request.method == 'POST':
        ruc = request.POST.get('ruc')
        razon_social = request.POST.get('razon_social')
        contacto = request.POST.get('contacto')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')

        Proveedor.objects.create(
            ruc=ruc,
            razon_social=razon_social,
            contacto=contacto,
            telefono=telefono,
            email=email,
            created_by=request.user
        )
        return redirect('dashboard_proveedores')

    query = request.GET.get('q', '')
    if query:
        proveedores = Proveedor.objects.filter(
            Q(ruc__icontains=query) | Q(razon_social__icontains=query)
        )
    else:
        proveedores = Proveedor.objects.all()

    context = {
        'proveedores': proveedores,
        'query': query,
    }
    return render(request, 'proveedores/dashboard_proveedores.html', context)
