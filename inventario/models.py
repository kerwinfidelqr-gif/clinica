from django.db import models
from django.conf import settings
from django.utils import timezone

# CATEGORÍAS
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# PRODUCTO
class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código del Producto")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos', verbose_name="Categoría")
    
    # Control de Stock
    stock_actual = models.IntegerField(default=0, verbose_name="Stock Actual")
    stock_minimo = models.IntegerField(default=5, verbose_name="Stock Mínimo") # Para encender la alerta roja en el diseño de Celina
    
    # Valores
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    
    # Estado
    estado = models.BooleanField(default=True, verbose_name="Activo")
    
    # Quién lo creó y cuándo
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    # Esta función matemática le dirá a la tarjeta de Celina si hay "Bajo Stock"
    def esta_en_bajo_stock(self):
        return self.stock_actual <= self.stock_minimo

# MOVIMIENTO de Entrada y Salida
class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    ]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo de Movimiento")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    motivo = models.CharField(max_length=255, verbose_name="Motivo")
    
    # Quien sacó o metio productos
    fecha_movimiento = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        ordering = ['-fecha_movimiento']

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"