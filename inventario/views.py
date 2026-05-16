from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Producto, Categoria
from .forms import ProductoForm

@login_required
def inventario_dashboard(request):
    # Inicializar el formulario
    form = ProductoForm()

    # PROCESAR EL REGISTRO
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            
            # Algoritmo meticuloso para autogenerar el código único del producto (Ej: MED-0013)
            ultimo_producto = Producto.objects.order_by('-id').first()
            siguiente_numero = (ultimo_producto.id + 1) if ultimo_producto else 1
            producto.codigo = f"MED-{siguiente_numero:04d}" # Genera formatos como MED-0001, MED-0002...
            
            # Asignar o crear la categoría automáticamente
            categoria_nombre = request.POST.get('categoria_nombre')
            if categoria_nombre:
                categoria, created = Categoria.objects.get_or_create(nombre=categoria_nombre)
                producto.categoria = categoria

            # Asignamos el usuario que está logueado en la clínica como creador
            producto.created_by = request.user
            producto.save()
            
            # Redirecciona a la misma página para limpiar el formulario y ver el nuevo producto
            return redirect('lista_dashboard')

    # FILTRAR LOS PRODUCTOS
    productos = Producto.objects.all()

    query = request.GET.get('q', '')
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(codigo__icontains=query)
        )

    categoria_filtro = request.GET.get('categoria', '')
    if categoria_filtro:
        productos = productos.filter(categoria__nombre__iexact=categoria_filtro)

    # ENVIAR TODA LA INFORMACIÓN
    context = {
        'productos': productos,
        'form': form,
        'query': query,
        'categoria_filtro': categoria_filtro,
    }
    return render(request, 'inventario/lista_dashboard.html', context)