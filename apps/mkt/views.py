# Python
import decimal
import uuid
# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q
from django.views.generic.base import TemplateView
from django.core.exceptions import ValidationError
# app mkt
from .cart import Cart
from .forms import fRegistroProducto, fExtra_Imagenes
from .models import Productos, Imagenes, Ventas, Envios
# app users
from apps.users.models import Direcciones
from apps.users.forms import fRegistroDirecciones
# app payment
from apps.payment.stripe import PaymentStripe, SimpleStripe
# app utils
from utils.models.operations import get_percent, get_iva

class CondicionesUso(TemplateView):
    template_name = 'mkt/condiciones_uso.html'

def vHome(request):
    productos = Productos.objects.filter(activo = True)
    return render(request, 'mkt/home.html', {'productos': productos})

def vProducto(request, slug, uuid):
    producto = get_object_or_404(Productos, uuid = uuid)
    return render(request, 'mkt/producto.html', {'producto': producto})

class SearchProduct(ListView):
    template_name = 'mkt/search.html'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        lookup = (Q(nombre__icontains = q) | Q(folio__icontains = q))
        productos = Productos.objects.filter(lookup, activo = True)
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

# checar que esté logueado
def vPagarCarrito(request):
    # initializing variables
    simple_stripe = SimpleStripe(request.user)
    cart_obj = Cart(request)
    fdireccion = fRegistroDirecciones(label_suffix = '')
    total = 0
    shipping_cost = decimal.Decimal(43.10)
    cards = simple_stripe.get_customer_cards()
    cart = cart_obj.cart
    uuid_list = list(cart)
    good_uuid_list = []
    # checking if cart has correct uuid
    for pdt_uuid in uuid_list:
        if check_uuid(pdt_uuid):
            good_uuid_list.append(pdt_uuid)
    # getting products from model
    products = Productos.objects.filter(uuid__in = good_uuid_list)
    # calc price quantity * product quantity 
    for p in products:
        item = cart.get(str(p.uuid))
        if item is not None:
            try:
                item_quantity = int(item.get('pdt_quantity', 1))
                # restar o remover del carrito si no hay en existencia (luego)----
                if item_quantity <= p.cantidad:
                    total = total + (item_quantity * p.get_public_price())
                    item.update({'stock': str(p.cantidad)})
                # -----
            except (TypeError, ValueError):
                cart_obj.remove(p)
                messages.error(request, 'No hemos podido verificar la información del producto <b>{}</b> por lo que lo hemos removido del carrito para que no sea cobrado'.format(p.nombre))
    # calc price + shipping + stripe
    shipping_cost = round(get_iva(shipping_cost) + shipping_cost, 2)
    total = total + shipping_cost
    total = total + simple_stripe.stripe_cost(total)
    show_payment = True if len(cart) > 0 else False
    if request.method == 'POST':
        payment = PaymentStripe(request.user)
        address = request.POST.get('address', '')
        card = request.POST.get('card', '')
        token = request.POST.get('stripeToken', '')
        save_card = request.POST.get('save-card', False)
        sale = None
        charge = None
        try:
            address = request.user.direcciones.get(uuid = address)
            sale = Ventas.objects.create(total = total, usuario = request.user)
            if isinstance(sale, Ventas):
                if token:
                    # componer aquí después-----
                    tok = token
                    if save_card:
                        new_card = payment.add_customer_card(token)
                        if new_card is not None:
                            tok = new_card['id']
                            charge = payment.make_charge(amount = int(total*100), token = tok, invoice = sale.folio, customer = payment.customer, request = request)
                        else:
                            charge = payment.make_charge(amount = int(total*100), token = tok, invoice = sale.folio, request = request)
                    else:
                        charge = payment.make_charge(amount = int(total*100), token = tok, invoice = sale.folio, request = request)
                    # -------
                elif card:
                    cus_card = payment.customer_card_exists(card)
                    if cus_card:
                        charge = payment.make_charge(amount = int(total*100), token = card, invoice = sale.folio, customer = payment.customer, request = request)
                    else:
                        messages.error(request, 'La tarjeta guardada seleccionada no existe. Por favor intente con otra o agregue otro método de pago')
                        return redirect('mkt:pagarCarrito')
                else:
                    messages.error(request, 'No se proporcionó ningún método de pago')
                    return redirect('mkt:pagarCarrito')
                if charge is not None:
                    if charge['status'] == 'succeeded':
                        sale.id_payment = charge['id']
                        sale.save(update_fields = ['id_payment'])
                        for p in products:
                            try:
                                item = cart.get(str(p.uuid))
                                if item is not None:
                                    item_quantity = item.get('pdt_quantity', 1)
                                    sale.productos.add(p, through_defaults = {'precio': p.get_public_price(), 'cantidad': item_quantity})
                                    # delete quantity from product stock
                                    p.cantidad = p.cantidad - item_quantity
                                    p.save()
                            except (TypeError, ValueError):
                                continue                    
                        request.session["cart"] = {}
                        request.session.modified = True
                        Envios.objects.create(venta = sale, direccion = address, direccion_txt = 'Calle: {}, no. int.:{}, no. ext.:{}, colonia:{}, c.p.:{}, referencias:{}, instrucciones:{}'.format(address.calle, address.no_interior, address.no_calle, address.colonia, address.codigo_postal, address.referencias, address.instrucciones))
                        request.user.send_payment_success(request.user, sale.folio)
                        return render(request, 'mkt/success_payment.html')
                    else:
                        sale.delete()
                        messages.error(request, 'No se ha podido procesar el pago. Inténtelo de nuevo <small>(error 001)</small>')
                else:
                    sale.delete()
                    messages.error(request, 'No se ha podido procesar el pago. Inténtelo de nuevo <small>(error 002)</small>')
            else:
                messages.error(request, 'No se ha podido procesar el pago. Inténtelo de nuevo <small>(error 003)</small>')
        except Direcciones.DoesNotExist:
            messages.error(request, 'Por favor selecciona una dirección de envío')
        except Exception as e:
            print(e)
            messages.error(request, 'No se ha podido procesar el pago. Inténtelo de nuevo <small>(error 004)</small>')
        return redirect('mkt:pagarCarrito')    
    context = {'cart': cart, 'total': total, 'fdireccion': fdireccion, 'show_payment': show_payment, 'cards': cards, 'shipping_cost': shipping_cost}
    return render(request, 'mkt/pago.html', context)

def check_uuid(value):
    if value is not None and not isinstance(value, uuid.UUID):
        input_form = 'int' if isinstance(value, int) else 'hex'
        try:
            uuid.UUID(**{input_form: value})
            return True
        except (AttributeError, ValueError):
            return False
    return value