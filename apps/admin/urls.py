# Django
from django.urls import path
# app admin
from .views import vAdmin, vLogin, vLogout, CreateProduct, ListProducts, ListSales, ListShipping, UpdateProduct, ListUsers

app_name = 'admin'

urlpatterns = [
    path('login', vLogin, name = 'login'),
    path('logout', vLogout, name = 'logout'),
    path('', vAdmin.as_view(), name = 'home'),
    path('registrar/producto', CreateProduct.as_view(), name = 'create_product'),
    path('editar/producto/<int:pk>/<slug:slug>', UpdateProduct.as_view(), name = 'update_product'),
    path('listar/productos', ListProducts.as_view(), name = 'list_products'),
    path('listar/ventas', ListSales.as_view(), name = 'list_sales'),
    path('listar/envios', ListShipping.as_view(), name = 'list_shipping'),
    path('listar/usuarios', ListUsers.as_view(), name = 'list_users')
]