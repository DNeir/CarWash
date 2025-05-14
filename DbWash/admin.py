from django.contrib import admin
from .models import Empleado, Cliente, Vehiculo, servicio, Cita
# Register your models here.

admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(servicio)
admin.site.register(Cita)