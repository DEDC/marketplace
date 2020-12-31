from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import fRegistroUsuarios, fLogin

def vRegistro(request):
    if request.method == 'POST':
        redirect_url = request.GET.get('redirect_url', None)
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
            print(fusuario.errors)
    else:
        fusuario = fRegistroUsuarios(label_suffix = '')
    context = {'fusuario': fusuario}
    return render(request, 'users/registro.html', context)

def vLogin(request):
    if request.method == 'POST':
        redirect_url = request.GET.get('redirect_url', None)
        flogin = fLogin(request.POST, label_suffix = '')
        if flogin.is_valid():
            username = flogin.cleaned_data['username']
            password = flogin.cleaned_data['password']
            autenticar = authenticate(username = username, password = password)
            if autenticar is not None:
                login(request, autenticar)
                return redirect(redirect_url) if redirect_url is not None else redirect('mkt:marketplace')
            else:
                messages.error(request, 'Usuario y/o contraseña no válidos')
        else:
            messages.error(request, 'Formulario inválido. Por favor corrija los errores marcados en rojo')
    else:
        flogin = fLogin()
    context = {'flogin': flogin}
    return render(request, 'users/login.html', context)

def vLogout(request):
    logout(request)
    return redirect('mkt:marketplace')