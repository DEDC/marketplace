# Django
from django.db.models import Sum, F, FloatField
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.views.generic.list import ListView
# app users
from .forms import fRegistroUsuarios, fLogin, fRegistroDirecciones
# app ventas
from apps.mkt.models import Ventas

def vRegistro(request):
    if request.method == 'POST':
        redirect_url = request.GET.get('redirect_to', None)
        fusuario = fRegistroUsuarios(request.POST, label_suffix = '')
        if fusuario.is_valid():
            usuario = fusuario.save(commit = False)
            usuario.set_password(usuario.password)
            usuario.is_active = True
            usuario.save()
            autenticar = authenticate(username = fusuario.cleaned_data['email'], password = fusuario.cleaned_data['password'])
            login(request, autenticar)
            messages.success(request, 'Registro de usuario con éxito')
            return redirect(redirect_url) if redirect_url is not None else redirect('mkt:marketplace')
        else:
            messages.error(request, 'Formulario inválido. Por favor corrija los errores marcados en rojo')
    else:
        fusuario = fRegistroUsuarios(label_suffix = '')
    context = {'fusuario': fusuario}
    return render(request, 'users/registro.html', context)

def vLogin(request):
    if request.method == 'POST':
        redirect_url = request.GET.get('redirect_to', None)
        flogin = fLogin(request.POST, label_suffix = '')
        if flogin.is_valid():
            username = flogin.cleaned_data['username']
            password = flogin.cleaned_data['password']
            autenticar = authenticate(username = username, password = password)
            if autenticar is not None:
                login(request, autenticar)
                messages.success(request, 'Bienvenido!, haz iniciado sesión.')
            else:
                messages.error(request, 'Usuario y/o contraseña no válidos')
        else:
            messages.error(request, 'Formulario inválido. Por favor corrija los errores marcados en rojo')
        return redirect(redirect_url) if redirect_url is not None else redirect('mkt:marketplace')

def vLogout(request):
    logout(request)
    messages.warning(request, 'Haz cerrado sesión')
    return redirect('mkt:marketplace')

def vDirecciones(request):
    if request.method == 'POST':
        redirect_url = request.GET.get('redirect_to', None)
        fdireccion = fRegistroDirecciones(request.POST, label_suffix = '')
        if fdireccion.is_valid():
            direccion = fdireccion.save(commit = False)
            direccion.usuario = request.user
            direccion.save()
            messages.success(request, 'Ha agregado una dirección de envío')
        else:
            messages.error(request, 'Formulario inválido. Por favor corrija los errores marcados en rojo')
    return redirect(redirect_url) if redirect_url is not None else redirect('mkt:marketplace')    

class ListOrders(ListView):
    model = Ventas
    template_name = 'users/pedidos.html'

    def get_queryset(self):
        queryset = (Ventas.objects.filter(usuario = self.request.user).annotate(total_sum = Sum(F('pdt_ventas__precio') * F('pdt_ventas__cantidad'), output_field = FloatField())))
        return queryset