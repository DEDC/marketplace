# Python
import decimal
# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q
# app mkt
from .cart import Cart
from .payment import PaymentStripe
from apps.mkt.forms import fRegistroProducto, fExtra_Imagenes
from apps.users.forms import fRegistroDirecciones
from apps.mkt.models import Productos, Imagenes, Ventas, Envios
# app users
from apps.users.models import Direcciones

def vHome(request):
    productos = Productos.objects.all()
    return render(request, 'mkt/home.html', {'productos': productos})

def vProducto(request, slug, uuid):
    producto = get_object_or_404(Productos, uuid = uuid)
    return render(request, 'mkt/producto.html', {'producto': producto})

class SearchProduct(ListView):
    template_name = 'mkt/search.html'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        lookup = (Q(nombre__icontains = q) | Q(folio__icontains = q))
        productos = Productos.objects.filter(lookup)
        return productos
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = self.get_queryset()
        context['q'] = self.request.GET.get('q', '')
        return context

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
        address = request.POST.get('address', '')
        try:
            address = request.user.direcciones.get(uuid = address)
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
                # limpiar el carrito
                request.session["cart"] = {}
                request.session.modified = True
                # crear el envio
                Envios.objects.create(venta = venta, direccion = address, 
                    direccion_txt = 'Calle: {}, no. int.:{}, no. ext.:{}, colonia:{}, c.p.:{}, referencias:{}, instrucciones:{}'.format(
                        address.calle, 
                        address.no_interior,
                        address.no_calle,
                        address.colonia,
                        address.codigo_postal,
                        address.referencias,
                        address.instrucciones
                    )
                )
        except Direcciones.DoesNotExist:
            messages.error(request, 'Por favor selecciona una dirección de envío')
        return redirect('mkt:pagarCarrito')
    fdireccion = fRegistroDirecciones(label_suffix = '')
    context = {'cart': cart, 'total': total, 'fdireccion': fdireccion}
    return render(request, 'mkt/pago.html', context)