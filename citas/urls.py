from django.urls import path
from . import views

urlpatterns = [

    path('', views.citas_dashboard, name='dashboard_cita'),
]