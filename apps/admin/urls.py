from django.urls import path
from apps.admin.views import CreateProduct, ListProducts
from .views import vAdmin

app_name = 'admin'

urlpatterns = [
    path('', vAdmin.as_view(), name = 'home'),
    path('registrar/producto', CreateProduct.as_view(), name = 'create_product'),
    path('listar/productos', ListProducts.as_view(), name = 'list_products')
]