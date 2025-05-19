from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from DbWash.models import Empleado, Cliente, Vehiculo, servicio, Cita
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    # Obtener las próximas 5 citas
    citas = Cita.objects.filter(estado='Pendiente').order_by('fecha_hora')[:5]
    # Obtener los 5 servicios más destacados (puedes ajustar este criterio)
    servicios = servicio.objects.all()[:5]
    
    context = {
        'citas': citas,
        'servicios': servicios
    }
    return render(request, 'index.html', context)


def empleados(request):
    return render(request, 'empleados.html', {})

def citas(request):
    # Parámetros de filtrado
    fecha = request.GET.get('fecha', '')
    estado = request.GET.get('estado', '')
    cliente_query = request.GET.get('cliente', '')
    
    # Consulta base
    citas_list = Cita.objects.all().order_by('-fecha_hora')
    
    # Aplicar filtros si existen
    if fecha:
        citas_list = citas_list.filter(fecha_hora__date=fecha)
    
    if estado:
        citas_list = citas_list.filter(estado=estado)
    
    if cliente_query:
        # Buscar por nombre de cliente (requiere join desde Cita -> Vehiculo -> Cliente)
        citas_list = citas_list.filter(
            Q(vehiculo__cliente__nombre__icontains=cliente_query) | 
            Q(vehiculo__cliente__cedula__icontains=cliente_query)
        )
    
    # Paginación
    paginator = Paginator(citas_list, 10)  # 10 citas por página
    page = request.GET.get('page')
    citas = paginator.get_page(page)
    
    # Obtener todos los clientes y servicios para los formularios
    clientes = Cliente.objects.all()
    servicios_list = servicio.objects.all()
    vehiculos = Vehiculo.objects.all()
    
    context = {
        'citas': citas,
        'clientes': clientes,
        'servicios': servicios_list,
        'vehiculos': vehiculos,
    }
    
    return render(request, 'citas.html', context)

def cita_crear(request):
    if request.method == 'POST':
        vehiculo_id = request.POST.get('vehiculo')
        servicio_ids = request.POST.getlist('servicio')
        fecha_hora = request.POST.get('fecha_hora')
        notas = request.POST.get('notas', '')
        
        # Asignar empleado (puedes implementar una lógica más compleja)
        # Por ejemplo, asignar al empleado con menos citas ese día
        empleado = Empleado.objects.first()
        
        if vehiculo_id and servicio_ids and fecha_hora and empleado:
            try:
                vehiculo = Vehiculo.objects.get(id=vehiculo_id)
                
                # Crear la cita
                cita = Cita.objects.create(
                    vehiculo=vehiculo,
                    empleado=empleado,
                    fecha_hora=fecha_hora,
                    estado='Pendiente',
                )
                
                # Agregar los servicios seleccionados
                for servicio_id in servicio_ids:
                    servicio_obj = servicio.objects.get(id=servicio_id)
                    cita.servicios.add(servicio_obj)
                
                messages.success(request, f'Cita creada exitosamente para el {fecha_hora}')
                return redirect('citas')
            except Exception as e:
                messages.error(request, f'Error al crear la cita: {str(e)}')
        else:
            messages.error(request, 'Faltan datos requeridos para crear la cita')
    
    return redirect('citas')

def cita_editar(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    
    if request.method == 'POST':
        vehiculo_id = request.POST.get('vehiculo')
        servicio_ids = request.POST.getlist('servicio')
        fecha_hora = request.POST.get('fecha_hora')
        estado = request.POST.get('estado')
        notas = request.POST.get('notas', '')
        
        try:
            # Actualizar la cita
            cita.vehiculo = Vehiculo.objects.get(id=vehiculo_id)
            cita.fecha_hora = fecha_hora
            cita.estado = estado
            cita.save()
            
            # Actualizar los servicios
            cita.servicios.clear()
            for servicio_id in servicio_ids:
                servicio_obj = servicio.objects.get(id=servicio_id)
                cita.servicios.add(servicio_obj)
            
            messages.success(request, 'Cita actualizada exitosamente')
        except Exception as e:
            messages.error(request, f'Error al actualizar la cita: {str(e)}')
    
    return redirect('citas')

def cita_eliminar(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    
    if request.method == 'POST':
        try:
            cita.delete()
            messages.success(request, 'Cita eliminada exitosamente')
        except Exception as e:
            messages.error(request, f'Error al eliminar la cita: {str(e)}')
    
    return redirect('citas')

def cita_detalle(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    context = {'cita': cita}
    return render(request, 'cita_detalle.html', context)

@csrf_exempt
def vehiculos_por_cliente(request, cliente_id):
    vehiculos = Vehiculo.objects.filter(cliente_id=cliente_id)
    data = list(vehiculos.values('id', 'marca', 'modelo', 'placa'))
    return JsonResponse(data, safe=False)

def bodega(request):    
    return render(request, 'bodega.html', {})