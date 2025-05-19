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
                    notas=notas
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
            # Actualizar la cita con el vehículo seleccionado
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
            cita.vehiculo = vehiculo
            cita.fecha_hora = fecha_hora
            cita.estado = estado
            cita.notas = notas
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
    empleados = Empleado.objects.all()
    servicios = servicio.objects.all()
    
    context = {
        'cita': cita,
        'empleados': empleados,
        'servicios': servicios
    }
    return render(request, 'cita_detalle.html', context)

def bodega(request):
    # Parámetros de filtrado para clientes
    nombre_cliente = request.GET.get('nombre_cliente', '')
    cedula = request.GET.get('cedula', '')
    
    # Parámetros de filtrado para vehículos
    placa = request.GET.get('placa', '')
    marca = request.GET.get('marca', '')
    cliente_nombre = request.GET.get('cliente_nombre', '')
    
    # Tab activo
    tab = request.GET.get('tab', 'clientes')
    
    # Consulta base para clientes
    clientes_list = Cliente.objects.all().order_by('nombre')
    
    # Aplicar filtros si existen para clientes
    if nombre_cliente:
        clientes_list = clientes_list.filter(nombre__icontains=nombre_cliente)
    
    if cedula:
        clientes_list = clientes_list.filter(cedula__icontains=cedula)
    
    # Consulta base para vehículos
    vehiculos_list = Vehiculo.objects.all().order_by('marca', 'modelo')
    
    # Aplicar filtros si existen para vehículos
    if placa:
        vehiculos_list = vehiculos_list.filter(placa__icontains=placa)
    
    if marca:
        vehiculos_list = vehiculos_list.filter(marca__icontains=marca)
    
    if cliente_nombre:
        vehiculos_list = vehiculos_list.filter(cliente__nombre__icontains=cliente_nombre)
    
    # Paginación para clientes
    paginator_clientes = Paginator(clientes_list, 10)
    page_clientes = request.GET.get('page')
    clientes = paginator_clientes.get_page(page_clientes)
    
    # Paginación para vehículos
    paginator_vehiculos = Paginator(vehiculos_list, 10)
    page_vehiculos = request.GET.get('page')
    vehiculos = paginator_vehiculos.get_page(page_vehiculos)
    
    context = {
        'clientes': clientes,
        'vehiculos': vehiculos,
        'tab': tab
    }
    
    return render(request, 'bodega.html', context)

def cliente_crear(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cedula = request.POST.get('cedula')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        
        if nombre and cedula and direccion and telefono and correo:
            try:
                # Verificar si ya existe un cliente con esa cédula
                if Cliente.objects.filter(cedula=cedula).exists():
                    messages.warning(request, f'Ya existe un cliente con la cédula {cedula}')
                    return redirect('bodega')
                
                # Crear el cliente
                cliente = Cliente.objects.create(
                    nombre=nombre,
                    cedula=cedula,
                    direccion=direccion,
                    telefono=telefono,
                    correo=correo
                )
                
                messages.success(request, f'Cliente {nombre} creado exitosamente')
            except Exception as e:
                messages.error(request, f'Error al crear el cliente: {str(e)}')
        else:
            messages.error(request, 'Faltan datos requeridos para crear el cliente')
    
    return redirect('bodega')

def cliente_editar(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cedula = request.POST.get('cedula')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        
        if nombre and cedula and direccion and telefono and correo:
            try:
                # Verificar si ya existe otro cliente con esa cédula
                if Cliente.objects.filter(cedula=cedula).exclude(id=cliente_id).exists():
                    messages.warning(request, f'Ya existe otro cliente con la cédula {cedula}')
                    return redirect('bodega')
                
                # Actualizar el cliente
                cliente.nombre = nombre
                cliente.cedula = cedula
                cliente.direccion = direccion
                cliente.telefono = telefono
                cliente.correo = correo
                cliente.save()
                
                messages.success(request, f'Cliente {nombre} actualizado exitosamente')
            except Exception as e:
                messages.error(request, f'Error al actualizar el cliente: {str(e)}')
        else:
            messages.error(request, 'Faltan datos requeridos para actualizar el cliente')
    
    return redirect('bodega')

def cliente_eliminar(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        try:
            nombre = cliente.nombre
            cliente.delete()
            messages.success(request, f'Cliente {nombre} eliminado exitosamente')
        except Exception as e:
            messages.error(request, f'Error al eliminar el cliente: {str(e)}')
    
    return redirect('bodega')

def vehiculo_crear(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        placa = request.POST.get('placa')
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        color = request.POST.get('color')
        tipo = request.POST.get('tipo')
        
        if cliente_id and placa and marca and modelo and color and tipo:
            try:
                # Verificar si ya existe un vehículo con esa placa
                if Vehiculo.objects.filter(placa=placa).exists():
                    messages.warning(request, f'Ya existe un vehículo con la placa {placa}')
                    return redirect('bodega')
                
                cliente = Cliente.objects.get(id=cliente_id)
                
                # Crear el vehículo
                vehiculo = Vehiculo.objects.create(
                    cliente=cliente,
                    placa=placa,
                    marca=marca,
                    modelo=modelo,
                    color=color,
                    tipo=tipo
                )
                
                messages.success(request, f'Vehículo {marca} {modelo} ({placa}) creado exitosamente')
            except Exception as e:
                messages.error(request, f'Error al crear el vehículo: {str(e)}')
        else:
            messages.error(request, 'Faltan datos requeridos para crear el vehículo')
    
    return redirect('bodega')

def vehiculo_editar(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        placa = request.POST.get('placa')
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        color = request.POST.get('color')
        tipo = request.POST.get('tipo')
        
        if cliente_id and placa and marca and modelo and color and tipo:
            try:
                # Verificar si ya existe otro vehículo con esa placa
                if Vehiculo.objects.filter(placa=placa).exclude(id=vehiculo_id).exists():
                    messages.warning(request, f'Ya existe otro vehículo con la placa {placa}')
                    return redirect('bodega')
                
                cliente = Cliente.objects.get(id=cliente_id)
                
                # Actualizar el vehículo
                vehiculo.cliente = cliente
                vehiculo.placa = placa
                vehiculo.marca = marca
                vehiculo.modelo = modelo
                vehiculo.color = color
                vehiculo.tipo = tipo
                vehiculo.save()
                
                messages.success(request, f'Vehículo {marca} {modelo} ({placa}) actualizado exitosamente')
            except Exception as e:
                messages.error(request, f'Error al actualizar el vehículo: {str(e)}')
        else:
            messages.error(request, 'Faltan datos requeridos para actualizar el vehículo')
    
    return redirect('bodega')

def vehiculo_eliminar(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    
    if request.method == 'POST':
        try:
            placa = vehiculo.placa
            vehiculo.delete()
            messages.success(request, f'Vehículo con placa {placa} eliminado exitosamente')
        except Exception as e:
            messages.error(request, f'Error al eliminar el vehículo: {str(e)}')
    
    return redirect('bodega')

@csrf_exempt
def vehiculos_por_cliente(request, cliente_id):
    vehiculos = Vehiculo.objects.filter(cliente_id=cliente_id)
    data = [
        {
            'id': v.id,
            'placa': v.placa,
            'marca': v.marca,
            'modelo': v.modelo,
        }
        for v in vehiculos
    ]
    return JsonResponse(data, safe=False)