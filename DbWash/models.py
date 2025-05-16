from django.db import models

# Create your models here.

class Empleado(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    telefono = models.CharField(max_length=15, null=False)
    puesto = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nombre
    
class Cliente(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    cedula = models.CharField(max_length=15, null=False)
    direccion = models.CharField(max_length=200, null=False)
    telefono = models.CharField(max_length=15, null=False)
    correo = models.EmailField(max_length=100, null=False)

    def __str__(self):
        return self.nombre
    

class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    placa = models.CharField(max_length=10, null=False)
    marca = models.CharField(max_length=50, null=False)
    modelo = models.CharField(max_length=50, null=False)
    color = models.CharField(max_length=30, null=False)
    tipo = models.CharField(max_length=30, null=False)
    

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"
    
class servicio(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Cita(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(null=False)
    servicios = models.ManyToManyField(servicio)
    estado = models.CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('Completada', 'Completada')], default='Pendiente')
    def __str__(self):
        return f"Cita para {self.vehiculo} con {self.empleado} el {self.fecha_hora}, estado: {self.estado} precio: {self.servicios.all()}" 