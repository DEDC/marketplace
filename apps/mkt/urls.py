# Django
from django.conf.urls import handler404
from django.urls import path
# app mkt
from .views import vHome, vAgregarCarrito, vProducto, vAccionesCarrito, vLimpiarCarrito, vPagarCarrito, vComprar, SearchProduct

app_name = 'mkt'

urlpatterns = [
    path('', vHome, name = 'marketplace'),
    path('producto/<slug:slug>/<uuid:uuid>', vProducto, name = 'producto'),
    path('carrito/agregar/producto', vAgregarCarrito, name = 'agCarrito'),
    # path('carrito/desagregar/producto', vQuitarCarrito, name = 'desagCarrito'),
    path('carrito/act/producto', vAccionesCarrito, name = 'actCarrito'),
    path('carrito/limpiar', vLimpiarCarrito, name = 'limpCarrito'),
    path('carrito/pagar', vPagarCarrito, name = 'pagarCarrito'),
    path('comprar', vComprar, name = 'comprar'),
    path('search', SearchProduct.as_view(), name = 'search')
]