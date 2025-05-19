from . import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path( 'admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('empleados/', views.empleados, name='empleados'),
    path('citas/', views.citas, name='citas'),
    path('citas/crear/', views.cita_crear, name='cita_crear'),
    path('citas/editar/<int:cita_id>/', views.cita_editar, name='cita_editar'),
    path('citas/eliminar/<int:cita_id>/', views.cita_eliminar, name='cita_eliminar'),
    path('citas/detalle/<int:cita_id>/', views.cita_detalle, name='cita_detalle'),
    path('api/vehiculos-por-cliente/<int:cliente_id>/', views.vehiculos_por_cliente, name='vehiculos_por_cliente'),
    
    # URLs para la gestión de clientes y vehículos
    path('bodega/', views.bodega, name='bodega'),
    path('cliente/crear/', views.cliente_crear, name='cliente_crear'),
    path('cliente/editar/<int:cliente_id>/', views.cliente_editar, name='cliente_editar'),
    path('cliente/eliminar/<int:cliente_id>/', views.cliente_eliminar, name='cliente_eliminar'),
    path('vehiculo/crear/', views.vehiculo_crear, name='vehiculo_crear'),
    path('vehiculo/editar/<int:vehiculo_id>/', views.vehiculo_editar, name='vehiculo_editar'),
    path('vehiculo/eliminar/<int:vehiculo_id>/', views.vehiculo_eliminar, name='vehiculo_eliminar'),
]
