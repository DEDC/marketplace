# Django
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# app mkt
from apps.mkt.models import Productos, Ventas, Envios
# app users
from apps.users.models import Usuarios
from apps.users.forms import fLogin

class vAdmin(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('admin:login')
    redirect_field_name = 'redirect_to'

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        return render(request, 'admin/home.html')

def vLogin(request):
    if request.method == 'POST':
        flogin = fLogin(request.POST, label_suffix = '')
        if flogin.is_valid():
            username = flogin.cleaned_data['username']
            password = flogin.cleaned_data['password']
            autenticar = authenticate(username = username, password = password, admin = True)
            if autenticar is not None:
                login(request, autenticar)
                return redirect('admin:home')
            else:
                messages.error(request, 'Usuario y/o contraseña no válidos')
        else:
            messages.error(request, 'Formulario inválido. Por favor corrija los errores marcados en rojo')
        return redirect('admin:login')
    else:
        flogin = fLogin(label_suffix = '')
    context = {'flogin': flogin}
    return render(request, 'admin/login.html', context)

def vLogout(request):
    logout(request)
    messages.warning(request, 'Haz cerrado sesión')
    return redirect('admin:login')

# Products
class CreateProduct(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Productos
    fields = ['nombre', 'precio', 'cantidad', 'descripcion', 'imagen', 'comision', 'tipo_comision']
    template_name = 'admin/productos/registro.html'
    success_url = reverse_lazy('admin:create_product')
    success_message = 'Producto registrado existosamente'
    login_url = reverse_lazy('admin:login')
    redirect_field_name = 'redirect_to'

    def test_func(self):
        return self.request.user.is_superuser

    def form_invalid(self, form):
        messages.error(self.request, 'Formulario inválido. Por favor corrija los errores marcados en rojo.')
        return super().form_invalid(form)
    
class UpdateProduct(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Productos
    fields = ['nombre', 'precio', 'cantidad', 'descripcion', 'imagen', 'comision', 'tipo_comision']
    query_pk_and_slug = True
    success_url = reverse_lazy('admin:list_products')
    template_name = 'admin/productos/editar.html'
    success_message = 'Producto actualizado exitosamente'
    login_url = reverse_lazy('admin:login')
    redirect_field_name = 'redirect_to'

    def test_func(self):
        return self.request.user.is_superuser

class ListProducts(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Productos
    template_name = 'admin/productos/listar.html'
    login_url = reverse_lazy('admin:login')
    redirect_field_name = 'redirect_to'

    def test_func(self):
        return self.request.user.is_superuser

# Sales
class ListSales(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Ventas
    template_name = 'admin/ventas/listar.html'
    login_url = reverse_lazy('admin:login')
    redirect_field_name = 'redirect_to'

    def test_func(self):
        return self.request.user.is_superuser

# Shipping
class ListShipping(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Envios
    template_name = 'admin/envios/listar.html'
    login_url = reverse_lazy('admin:login')
    redirect_field_name = 'redirect_to'
    
    def test_func(self):
        return self.request.user.is_superuser

# Users
class ListUsers(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Usuarios
    template_name = 'admin/usuarios/listar.html'
    login_url = reverse_lazy('admin:login')
    redirect_field_name = 'redirect_to'

    def test_func(self):
        return self.request.user.is_superuser