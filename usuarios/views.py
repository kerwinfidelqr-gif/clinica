from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .formulario import Login
from .models import UsuarioRol, Rol

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = Login(request, data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=contrasenia)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Usuario o contraseña incorrecta.')
        else:
            messages.error(request, 'Usuario o contraseña incorrecta.')
    else:
        form = Login()
        
    return render(request, 'usuario/login.html' , {'form': form})
    
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión con éxito.')
    return redirect ('login')
