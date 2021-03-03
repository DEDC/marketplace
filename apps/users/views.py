# Django
from django.db.models import Sum, F, FloatField
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.views.generic.list import ListView
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from .user_tokens import account_activation_token
# app users
from .forms import fRegistroUsuarios, fLogin, fRegistroDirecciones, fResetPasswordEmail, fSetPasswordEmail
from .models import Usuarios
# app mkt
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
            sent = usuario.send_user_confirmation(request.user, request)
            if sent:
                messages.success(request, 'Registro de usuario exitoso')
            else:
                pass
            return redirect(redirect_url) if redirect_url is not None else redirect('mkt:marketplace')
        else:
            messages.error(request, 'Formulario inválido. Por favor corrija los errores marcados en rojo')
    return redirect('mkt:marketplace')

def vConfirmUser(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Usuarios.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Usuarios.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_confirmed = True
        user.save()
        messages.success(request, 'Su cuenta ha sido activada exitosamente. Ahora puede iniciar sesión. Gracias', extra_tags = 'email_confirmation')
    else:
        messages.error(request, 'No fue posible activar su cuenta con este enlace', extra_tags = 'email_confirmation')
    return redirect('mkt:marketplace')

def vResetPasswordEmail(request):
    if request.method == 'POST':
        fresetpass = fResetPasswordEmail(request.POST)
        if fresetpass.is_valid():
            try:
                user = Usuarios.objects.get(email = fresetpass.cleaned_data['email_reset'])
                sended = user.reset_password_email(user, request)
                if sended:
                    messages.success(request, 'Correo enviado exitosamente. Por favor revisa tu bandeja de entrada o spam')
                else:
                    messages.error(request, 'No hemos podido enviar un correo')
            except Usuarios.DoesNotExist:
                messages.error(request, 'Ese correo electrónico no se encuentra registrado')
        else:
            messages.error(request, 'Formulario inválido')
        return redirect('user:reset_password')
    else:
        fresetpass = fResetPasswordEmail()
    context = {'fresetpass': fresetpass}
    return render(request, 'users/reset_password.html', context)

def PasswordResetEmailConfirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = Usuarios.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuarios.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            fsetpass = fSetPasswordEmail(request.POST)
            if fsetpass.is_valid():
                new_password = fsetpass.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Tu contraseña ha sido cambiada exitosamente')
                return redirect('mkt:marketplace')
            else:
                messages.error(request, 'Por favor corrija los errores marcados en rojo')
        else:
            fsetpass = fSetPasswordEmail()
        context = {'fsetpass': fsetpass}
        return render(request, 'users/set_password.html', context)
    else:
        messages.error(request, 'El enlace ya no está disponible')
    return redirect('users:reset_password')

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