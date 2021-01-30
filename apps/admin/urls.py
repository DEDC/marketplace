from django.urls import path
from apps.mkt.views import vRegistroProductos
from .views import vAdmin

app_name = 'admin'

urlpatterns = [
    path('', vAdmin.as_view(), name = 'home'),
    path('registro/productos', vRegistroProductos, name = 'rProductos')
]