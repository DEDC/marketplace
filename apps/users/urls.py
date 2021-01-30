from django.urls import path
from .views import vLogin, vLogout, vRegistro, vDirecciones

app_name = 'user'

urlpatterns = [
    path('login/', vLogin, name = 'login'),
    path('logout/', vLogout, name = 'logout'),
    path('registro/', vRegistro, name = 'rUsuario'),
    path('agregar/direccion', vDirecciones, name = 'rDirecciones')
]