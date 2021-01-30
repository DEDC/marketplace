# Django
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
# app mkt
from apps.mkt.models import Productos

class vAdmin(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/home.html')

class CreateProduct(SuccessMessageMixin, CreateView):
    model = Productos
    fields = ['nombre', 'precio', 'cantidad', 'descripcion', 'imagen', 'comision', 'tipo_comision']
    template_name = 'admin/productos/registro.html'
    success_url = reverse_lazy('admin:create_product')
    success_message = 'Producto registrado existosamente'

    def form_invalid(self, form):
        messages.error(self.request, 'Formulario inválido. Por favor corrija los errores marcados en rojo.')
        return super().form_invalid(form)

class ListProducts(ListView):
    model = Productos
    template_name = 'admin/productos/listar.html'