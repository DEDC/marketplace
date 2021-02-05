from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .cart import Cart
from .payment import PaymentStripe
from apps.mkt.forms import fRegistroProducto, fExtra_Imagenes
from apps.users.forms import fRegistroDirecciones
from apps.mkt.models import Productos, Imagenes, Ventas, Envios
import decimal

def vHome(request):
    productos = Productos.objects.all()
    return render(request, 'mkt/home.html', {'productos': productos})

def vProducto(request, slug, uuid):
    producto = get_object_or_404(Productos, uuid = uuid)
    return render(request, 'mkt/producto.html', {'producto': producto})

def vRegistroProductos(request):
    if request.method == 'POST':
        fproducto = fRegistroProducto(request.POST, request.FILES, label_suffix = '')
        imagenes = request.FILES.getlist('imagen')
        if fproducto.is_valid():
            producto = fproducto.save()
            for imagen in imagenes:
                img = Imagenes(imagen = imagen)
                img.save()
            messages.success(request, 'Producto agregado exitosamente')
            return redirect('admin:rProductos')
        else:
            print(fproducto.errors)
            messages.error(request, 'Formulario inválido')
    else:
        fproducto = fRegistroProducto(label_suffix = '')
    context = {'fproducto': fproducto}
    return render(request, 'admin/productos/registro.html', context)

def vAgregarCarrito(request):
    if request.method == 'POST':
        pdt_uuid = request.POST.get('pdt-id', '')
        pdt_quantity = request.POST.get('pdt-quantity', 1)
        url_origin = request.POST.get('url-origin')
        try:
            producto = Productos.objects.get(uuid = pdt_uuid)
            cart = Cart(request)
            cart.add(producto, pdt_quantity)
            return redirect(url_origin)
        except Productos.DoesNotExist:
            pass
    return redirect('mkt:marketplace')

def vComprar(request):
    if request.method == 'POST':
        pdt_uuid = request.POST.get('pdt-id', '')
        pdt_quantity = request.POST.get('pdt-quantity', 1)
        url_origin = request.POST.get('url-origin')
        try:
            producto = Productos.objects.get(uuid = pdt_uuid)
            cart = Cart(request)
            cart.add(producto, pdt_quantity)
            return redirect('mkt:pagarCarrito')
        except Productos.DoesNotExist:
            pass
    return redirect('mkt:marketplace')


def vAccionesCarrito(request):
    if request.method == 'POST':
        pdt_uuid = request.POST.get('pdt-id', '')
        url_origin = request.POST.get('url-origin')
        try:
            producto = Productos.objects.get(uuid = pdt_uuid)
            cart = Cart(request)
            if request.POST.get('increment', None) is not None:
                cart.add(producto)
            elif request.POST.get('decrement', None) is not None:
                cart.decrement(producto)
            elif request.POST.get('remove', None) is not None:
                cart.remove(producto)
            elif request.POST.get('clear', None) is not None:
                cart.clear()
            return redirect(url_origin)
        except Productos.DoesNotExist:
            pass
    return redirect('mkt:marketplace')

def vLimpiarCarrito(request):
    if request.method == 'POST':
        url_origin = request.POST.get('url-origin')
        cart = Cart(request)
        cart.clear()
        return redirect(url_origin)
    return redirect('mkt:marketplace')

def vPagarCarrito(request):
    try:
        cart = request.session['cart']
        uuid_list = list(cart)
        productos = Productos.objects.filter(uuid__in = uuid_list)
        total = 0
        for p in productos:
            item = cart.get(str(p.uuid))
            total = total + (int(item['pdt_quantity']) * p.get_public_price())
            item.update({'stock': str(p.cantidad)})
    except KeyError:
        cart = []
    if request.method == 'POST':
        default_message = 'No especificado'
        token = request.POST.get('stripeToken', '')
        payment = PaymentStripe()
        charge = payment.make_charge(amount = int(total*100), token = token)
        if charge['status'] == 'succeeded':
            messages.success(request, 'Muchas gracias. Su compra se ha completado exitosamente.')
            # crear la venta
            venta = Ventas.objects.create(total = total, usuario = request.user)
            for p in productos:
                try:
                    item = cart.get(str(p.uuid))
                    venta.productos.add(p, through_defaults = {'precio': p.get_public_price(), 'cantidad': int(item['pdt_quantity'])})
                    # revisar aquí después +++++++++++++++++++
                    p.cantidad = p.cantidad - int(item['pdt_quantity'])
                    p.save()
                except KeyError:
                    continue
            # crear el envio
            Envios.objects.create(venta = venta)
            # limpiar el carrito
            request.session["cart"] = {}
            request.session.modified = True
        return redirect('mkt:pagarCarrito')
    fdireccion = fRegistroDirecciones(label_suffix = '')
    context = {'cart': cart, 'total': total, 'fdireccion': fdireccion}
    return render(request, 'mkt/pago.html', context)