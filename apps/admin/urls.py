from django.urls import path
from apps.mkt.views import vRegistroProductos
app_name = 'admin'

urlpatterns = [
    path('registro/productos', vRegistroProductos, name = 'rProductos')
]