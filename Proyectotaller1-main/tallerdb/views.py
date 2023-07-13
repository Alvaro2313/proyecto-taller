from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render,redirect
from .models import Cliente, Producto, Boleta, detalle_boleta
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from tallerdb.compra import Carrito
from django.shortcuts import render,redirect,get_object_or_404

def agregar_producto(request,id):
    carrito_compra= Carrito(request)
    producto =get_object_or_404 (Producto,id_producto=id)
    cantidad_restar = 1
    producto.stock -= cantidad_restar
    carrito_compra.agregar(producto=producto)
    producto.save()
    return redirect('tienda')

def eliminar_producto(request,id):
    carrito_compra= Carrito(request)
    producto = get_object_or_404 (Producto,id_producto=id)
    cantidad_restar = 1
    producto.stock += cantidad_restar
    carrito_compra.eliminar(producto=producto)

    return redirect('tienda')
def restar_producto(request,id):
    carrito_compra= Carrito(request)
    producto = get_object_or_404 (Producto,id_producto=id)
    cantidad_restar = 1
    producto.stock += cantidad_restar
    carrito_compra.restar(producto=producto)
    producto.save()
    return redirect('tienda')

def limpiar_carrito(request):
    carrito_compra = Carrito(request)
    carrito_compra.limpiar()
    return redirect('tienda')

def generarBoleta(request):
    precio_total=0
    for key,value in request.session['carrito'].items():
        precio_total = precio_total+ int(value['precio']) * int(value['cantidad'])
    boleta = Boleta(total = precio_total)
    boleta.save()
    productoss=[]
    for key,value in request.session['carrito'].items():
            producto = Producto.objects.get(id_producto = value['id_producto'])
            cant = value['cantidad']
            subtotal = cant * int(value['precio'])
            detalle = detalle_boleta(id_boleta = boleta, id_pro = producto, cantidad= cant, subtotal = subtotal)
            detalle.save()
            productoss.append(detalle)
    datos={
        'productos':productoss,
        'fecha':boleta.fechaCompra,
        'total':boleta.total
    }
    request.session['boleta']= boleta.id_boleta
    carrito= Carrito(request)
    carrito.limpiar()
    return render(request, 'tallerdb/detallecarrito.html',datos)



def tienda(request):
    return render(request, 'tallerdb/tienda.html')


def tienda(request):
    productos=Producto.objects.all()
    return render(request, 'tallerdb/tienda.html', {'productos':productos})


@login_required
def proyecto(request):
    context={}
    return render(request, 'tallerdb/proyecto.html', context)

def salir (request):
    logout(request)
    return redirect('/')

def index(request):
    return render(request,'tallerdb/paginacargaini.html')

def cambiomotor(request):
    return render(request, 'tallerdb/cambiodemotor.html')

def formulario(request):
    return render(request, 'tallerdb/formulario.html')

def equipo(request):
    return render(request, 'tallerdb/equipo.html')

def correo(request):
    return render(request, 'tallerdb/correo.html')

def inicio(request):
    return render(request, 'registration/login.html')
def edifor(request):
    return render(request, 'tallerdb/edicionfor.html')


def home(request):
    clientes = Cliente.objects.all()
    messages.success(request, '¡Clientes listados!')
    return render(request, 'tallerdb/clientes.html',{"clientes":clientes})
def registrarCliente(request):
    rut = request.POST['rut']
    nombre = request.POST['nombre']
    apellido_paterno = request.POST['apellido_paterno']
    apellido_materno = request.POST['apellido_materno']
    telefono = request.POST['telefono']
    email = request.POST['email']
    direccion = request.POST['direccion']
    activo = request.POST['activo']
    cliente = Cliente.objects.create(rut=rut, nombre=nombre, apellido_paterno=apellido_paterno,
                                     apellido_materno=apellido_materno,telefono=telefono,email=email,direccion=direccion,activo=activo)
    messages.success(request, '¡Cliente registrado!')
    return redirect('formulario')

def edicionCliente(request, rut):
    cliente = Cliente.objects.get(rut=rut)
    return render(request, "tallerdb/edicionfor.html", {"cliente": cliente})

def editarCliente(request):
    rut = request.POST['rut']
    nombre=request.POST['nombre']
    apellido_paterno = request.POST['apellido_paterno']
    apellido_materno = request.POST['apellido_materno']
    telefono = request.POST['telefono']
    email = request.POST['email']
    direccion = request.POST['direccion']
    activo = request.POST['activo']
    cliente=Cliente.objects.get(rut=rut)
    cliente.rut=rut
    cliente.nombre=nombre
    cliente.apellido_paterno=apellido_paterno
    cliente.apellido_materno=apellido_materno
    cliente.telefono=telefono
    cliente.email=email
    cliente.direccion=direccion
    cliente.activo=activo
    cliente.save()
    return redirect('/')

def eliminarCliente(request, rut):
    cliente = Cliente.objects.get(rut=rut)
    cliente.delete()

    messages.success(request, '¡Cliente eliminado!')

    return redirect('/')

