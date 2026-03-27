from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario

class Login(AuthenticationForm):
    username = forms.CharField(
        label = 'Usuario',
        widget= forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su usuario',
            'autocomplete': 'off'   
        })
    )

    password = forms.CharField(
        label = 'Contraseña',
        widget= forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'autocomplete': 'new-password'  
        })
    )

    class Meta:
        model = Usuario
        fields = ['username', 'password']