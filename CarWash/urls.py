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
    path('bodega/', views.bodega, name='bodega'),
]
