# Django
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
# app mkt
from apps.mkt.models import Productos, Ventas, Envios
# app users
from apps.users.models import Usuarios

class vAdmin(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/home.html')

# Products
class CreateProduct(SuccessMessageMixin, CreateView):
    model = Productos
    fields = ['nombre', 'precio', 'cantidad', 'descripcion', 'imagen', 'comision', 'tipo_comision']
    template_name = 'admin/productos/registro.html'
    success_url = reverse_lazy('admin:create_product')
    success_message = 'Producto registrado existosamente'

    def form_invalid(self, form):
        messages.error(self.request, 'Formulario inválido. Por favor corrija los errores marcados en rojo.')
        return super().form_invalid(form)
    
class UpdateProduct(SuccessMessageMixin, UpdateView):
    model = Productos
    fields = ['nombre', 'precio', 'cantidad', 'descripcion', 'imagen', 'comision', 'tipo_comision']
    query_pk_and_slug = True
    success_url = reverse_lazy('admin:list_products')
    template_name = 'admin/productos/editar.html'
    success_message = 'Producto actualizado exitosamente'

    # def get_success_url(self):
    #     return reverse_lazy('admin:update_product', kwargs={'pk': self.object.pk, 'slug': self.object.slug})

class ListProducts(ListView):
    model = Productos
    template_name = 'admin/productos/listar.html'

# Sales
class ListSales(ListView):
    model = Ventas
    template_name = 'admin/ventas/listar.html'

# Shipping
class ListShipping(ListView):
    model = Envios
    template_name = 'admin/envios/listar.html'

# Users
class ListUsers(ListView):
    model = Usuarios
    template_name = 'admin/usuarios/listar.html'