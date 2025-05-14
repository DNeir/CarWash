from django.shortcuts import render
from DbWash.models import Empleado, Cliente, Vehiculo, servicio, Cita

def index(request):
    return render(request, 'index.html', {})


def empleados(request):
    return render(request, 'empleados.html', {})

def citas(request):
    return render(request, 'citas.html', {})

def bodega(request):    
    return render(request, 'bodega.html', {})