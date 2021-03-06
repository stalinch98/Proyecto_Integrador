# Django
from django.shortcuts import render, redirect
from django.db.models import Q

# Local models
from admins.models import Reserva as r
from admins.models import Anuncios as a
from admins.models import Empresa as emp
from admins.models import Contacto as contact
from admins.models import Blog as bl
from admins.models import Imagen as im
from admins.models import Ubicacion as ub
from admins.models import Cotizar as cot
from admins.models import SubImagenes as subimg
from admins.models import Reserva as rv
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max


def QuienesSomos(request):
    mision = emp.objects.values( 'mision' )
    vision = emp.objects.values( 'vision' )

    for i in mision[0].values():
        mision2 = i

    for i in vision[0].values():
        vision2 = i

    datos = [
        {
            'mision': mision2,
            'vision': vision2
        }
    ]

    return render( request, 'housetime/quienes_somos.html', {'datos': datos} )


def Anuncios(request):
    anuncios = a.objects.filter( oferta=0 ).values()
    ubicaciones = ub.objects.all().values()
    imagenes = im.objects.all().values()

    return render( request, 'housetime/anuncios.html',
                   {'anuncios': anuncios, 'imagenes': imagenes, 'ubicaciones': ubicaciones} )


def Contacto(request):
    return render( request, 'housetime/contacto.html' )


def Promociones(request):
    promociones = a.objects.filter( oferta=1 ).values()
    imagenes = im.objects.all().values()
    return render( request, 'housetime/promociones.html', {'promociones': promociones, 'imagenes': imagenes} )


def Blog(request):
    descripcion = emp.objects.values( 'descripcion_blog' )
    opiniones = bl.objects.values( 'nombre_usuario', 'comentarios' ).order_by( '-id_blog' )

    for i in descripcion[0].values():
        descripcion2 = i

    blog = [
        {
            'blog': descripcion2,
        }
    ]
    return render( request, 'housetime/blog.html', {'blog': blog, 'opiniones': opiniones} )


def CompraDetalle(request):
    id = request.POST['id_anuncio']
    anuncio = a.objects.filter( id_anuncio=id ).values()
    coordenadas = ub.objects.filter( id_ubicacion=id ).values()
    imagen = im.objects.filter( id_imagen=id ).values()
    subimagenes = subimg.objects.filter( id_imagen=id ).values()
    return render( request, 'housetime/anuncio_detalle.html',
                   {'anuncio': anuncio, 'coordenadas': coordenadas, 'imagen': imagen, 'subimagenes': subimagenes} )


def get_housetime(request):
    cantClientes = r.objects.count()
    cantDepartamentos = a.objects.filter( id_tipo=2 ).count()
    cantCasas = a.objects.filter( id_tipo=1 ).count()
    cantPromociones = a.objects.filter( oferta=True ).count()

    inventario = [
        {
            'clientes': cantClientes,
            'casas': cantCasas,
            'departamentos': cantDepartamentos,
            'promociones': cantPromociones,
        }
    ]

    return render( request, 'housetime/index.html', {'inventario': inventario} )


def savecontact(request):
    contacto = contact()
    if request.method == 'POST':
        contacto.nombre_usuario = request.POST['nombre']
        contacto.celular = request.POST['telefono']
        contacto.email = request.POST['email']
        contacto.mensaje = request.POST['mensaje']
        contacto.save()
        return redirect( 'housetime' )
    else:
        contacto = contact()

    return render( request, 'housetime/contacto.html' )


def saveopinion(request):
    blog = bl()
    if request.method == 'POST':
        blog.nombre_usuario = request.POST['nombre']
        blog.comentarios = request.POST['mensaje']
        blog.save()
        return redirect( 'housetime' )
    else:
        blog = bl()

    return render( request, 'housetime/blog.html' )


def savecotizacion(request):
    cotizar = cot()
    if request.method == 'POST':
        opciones = []
        opciones.append( request.POST.get( 'Piscina' ) )
        opciones.append( request.POST.get( 'Parqueadero' ) )
        opciones.append( request.POST.get( 'Wifi' ) )
        opciones.append( request.POST.get( 'TV-Cable' ) )
        opciones.append( request.POST.get( 'Sauna' ) )
        opciones.append( request.POST.get( 'Hidromasaje' ) )
        opciones.append( request.POST.get( 'Room-Service' ) )
        for i in opciones:
            opciones.remove( None )

        cotizar.nombre = request.POST['nombre']
        cotizar.apellido = request.POST['apellido']
        cotizar.cedula = request.POST['cedula']
        cotizar.correo = request.POST['nombre']
        cotizar.opciones = opciones
        cotizar.save()
        return redirect( 'housetime' )
    else:
        cotizar = cot()

    return render( request, 'housetime/anuncios.html' )


def searchforname(request):
    nombre = request.POST['nombre']
    anuncios = a.objects.filter( Q( descripcion__contains=nombre ) & Q( oferta=0 ) ).values()
    imagenes = im.objects.all().values()

    return render( request, 'housetime/busqueda_nombre.html', {'anuncios': anuncios, 'imagenes': imagenes} )


def searchforprice(request):
    precio = request.POST['precio']
    anuncios = a.objects.filter( Q( precio_dia__lte=precio ) & Q( oferta=0 ) ).values()
    imagenes = im.objects.all().values()

    return render( request, 'housetime/busqueda_precio.html', {'anuncios': anuncios, 'imagenes': imagenes} )


def searchforubication(request):
    ubicacion = request.POST['ubicacion']
    anuncios = a.objects.filter( Q( id_ubicacion=ubicacion ) & Q( oferta=0 ) ).values()
    imagenes = im.objects.all().values()

    return render( request, 'housetime/busqueda_ubicacion.html', {'anuncios': anuncios, 'imagenes': imagenes} )


def searchforservices(request):
    servicios = []

    wifi = request.POST.get( 'Wifi' )
    parqueadero = request.POST.get( 'Parqueadero' )
    piscina = request.POST.get( 'Piscina' )
    sauna = request.POST.get( 'Sauna' )
    tvcable = request.POST.get( 'TV-Cable' )
    hidromasaje = request.POST.get( 'Hidromasaje' )
    room = request.POST.get( 'Room-Service' )
    opciones = str( wifi ) + "," + str( parqueadero ) + "," + str( piscina ) + "," + str( sauna ) + "," + str(
        tvcable ) + "," + str( hidromasaje ) + "," + str( room )

    opciones = opciones.replace( "None,", "" )
    opciones = opciones.replace( "None", "" )
    opciones = opciones.rstrip( ',' )

    anuncios = a.objects.filter( Q( servicios__contains=opciones ) & Q( oferta=0 ) ).values()
    imagenes = im.objects.all().values()

    return render( request, 'housetime/busqueda_servicios.html', {'anuncios': anuncios, 'imagenes': imagenes} )


def searchforcapacity(request):
    adultos = request.POST['n_adultos']
    ninos = request.POST['n_ninos']
    if adultos == '':
        adultos = 0
    if ninos == '':
        ninos = 0
    capacidad = int( adultos ) + int( ninos )
    print( capacidad )
    anuncios = a.objects.filter( Q( max_personas__lte=capacidad ) & Q( oferta=0 ) ).values()
    imagenes = im.objects.all().values()

    return render( request, 'housetime/busqueda_capacidad.html', {'anuncios': anuncios, 'imagenes': imagenes} )


def reservation(request):
    reserva = rv()
    anuncio = request.POST['id_anuncio']
    print( anuncio )
    precio = a.objects.filter( id_anuncio=anuncio ).values( 'precio_dia' )
    precio_oferta = a.objects.filter( id_anuncio=anuncio ).values( 'precio_oferta' )

    for i in precio:
        gato = i['precio_dia']

    for j in precio_oferta:
        perro = j['precio_oferta']

    if perro == None:
        precio_final = gato

    if perro != None:
        precio_final = perro

    if request.method == 'POST':
        valor = anuncio
        n_dias = request.POST['ndias']
        reserva.nombre = request.POST['nombres']
        reserva.cedula = request.POST['cedula']
        reserva.telefono = request.POST['celular']
        reserva.n_adultos = request.POST['nadultos']
        reserva.n_ninos = request.POST['nninos']
        reserva.n_dias = n_dias
        reserva.precio_total = float( precio_final ) * float( n_dias )
        reserva.id_anuncio_id = valor
        reserva.save()

        id = rv.objects.aggregate( Max( 'id_reserva' ) )
        id_reserv = id['id_reserva__max']
        reserv = rv.objects.filter( id_reserva=id_reserv ).values()
        producto = a.objects.filter( id_anuncio=valor ).values()

        for i in producto:
            img = i['id_imagen_id']

        photo = im.objects.filter( id_imagen=img ).values()
        return render( request, 'housetime/pagar.html', {'reserva': reserv, 'producto': producto, 'photo': photo} )
    else:
        reserva = rv()

    return render( request, 'housetime/anuncios.html' )


def home(request):
    item = request.POST['item']
    precio = request.POST['precio']
    paypal_dict = {
        "business": "joelsandoval1998@hotmail.com",
        "currency_code": "USD",
        "item_name": str( item ),
        "amount": str( precio ),
        "notify_url": "",
        "return_url": "",
        "cancel_return": "",
    }
    form = PayPalPaymentsForm( initial=paypal_dict )
    return render( request, 'housetime/paypal.html', {'form': form} )


@csrf_exempt
def paypal_return(request):
    args = {'post': request.POST, 'get': request.GET}
    return render( 'housetime/paypal_return.html', args )


def paypal_cancel(request):
    args = {'post': request.POST, 'get': request.GET}
    return render( 'housetime/paypal_cancel.html', args )
