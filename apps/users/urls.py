# django
from django.urls import path
# app users
from .views import vLogin, vLogout, vRegistro, vDirecciones

app_name = 'user'

urlpatterns = [
    path('login/', vLogin, name = 'login'),
    path('logout/', vLogout, name = 'logout'),
    path('registro/', vRegistro, name = 'rUsuario'),
    path('agregar/direccion', vDirecciones, name = 'rDirecciones')
]