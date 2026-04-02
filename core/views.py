from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache 

@login_required
@never_cache
def dashboard_view(request):
    
    # La validación de permisos y roles ahora se inyecta automáticamente 
    # a nivel global gracias a core/context_processors.py
    
    context = {
        'usuario': request.user,
    }

    return render(request, 'core/dashboard.html', context)