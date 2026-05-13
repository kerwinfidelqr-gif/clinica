from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard_proveedores, name='dashboard_proveedores'),
]