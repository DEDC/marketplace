from django.contrib import messages

class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart', {})
        self.cart = cart
    
    def add(self, item, quantity = 1):
        if str(item.uuid) not in self.cart.keys():
            self.cart[str(item.uuid)] = {
                'pdt_name': item.nombre,
                'pdt_quantity': quantity,
                'pdt_uuid': str(item.uuid),
                'pdt_slug': str(item.slug),
                'pdt_price': str(item.precio * int(quantity)),
                'pdt_image': item.imagen.url
            }
            messages.success(self.request, 'Se ha agregado un producto al carrito')
        else:
            for key, value in self.cart.items():
                if key == str(item.uuid):
                    if (int(value['pdt_quantity']) + int(quantity)) <= item.cantidad:
                        value['pdt_quantity'] = int(value['pdt_quantity']) + int(quantity)
                        value['pdt_price'] = str(item.precio * int(value['pdt_quantity']))
                        messages.success(self.request, 'Se ha agregado una unidad más al producto en el carrito')
                    else:
                        messages.warning(self.request, 'No hay más productos disponibles')
                    break
        self.save()
    
    def remove(self, item):
        uuid = str(item.uuid)
        if uuid in self.cart:
            del self.cart[uuid]
            self.save()
            messages.warning(self.request, 'Se ha removido el producto del carrito')
    
    def decrement(self, item):
        for key, value in self.cart.items():
            if key == str(item.uuid):
                value['pdt_quantity'] = value['pdt_quantity'] -1
                value['pdt_price'] = str(item.precio * int(value['pdt_quantity']))
                if value['pdt_quantity'] < 1:
                    self.remove(item)
                else:
                    self.save()
                    messages.warning(self.request, 'Se ha removido una unidad al producto en el carrito')
                break
    
    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True
        messages.warning(self.request, 'Se ha vaciado el carrito')

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True