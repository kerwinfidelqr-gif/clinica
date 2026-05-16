from django import forms
from .models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # Indicamos los campos
        fields = ['nombre', 'stock_actual', 'stock_minimo', 'precio_unitario']
        
        # Inyectar clases de Tailwind.
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-50 border border-gray-100 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#233b6e]/10 focus:border-[#233b6e] transition-all',
                'placeholder': 'Ej: Paracetamol 500mg...'
            }),
            'stock_actual': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-50 border border-gray-100 rounded-lg text-sm focus:outline-none focus:border-[#233b6e]',
                'placeholder': '0'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-50 border border-gray-100 rounded-lg text-sm focus:outline-none focus:border-[#233b6e]',
                'placeholder': 'Ej: 5'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-50 border border-gray-100 rounded-lg text-sm focus:outline-none focus:border-[#233b6e]',
                'placeholder': '0.00'
            }),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-50 border border-gray-100 rounded-lg text-sm focus:outline-none focus:border-[#233b6e]'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 bg-gray-50 border border-gray-100 rounded-lg text-sm focus:outline-none focus:border-[#233b6e]',
                'rows': 3
            }),
        }