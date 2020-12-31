from django.urls import path
from .views import vLogin, vLogout, vRegistro

app_name = 'user'

urlpatterns = [
    path('login/', vLogin, name = 'login'),
    path('logout/', vLogout, name = 'logout'),
    path('registro/', vRegistro, name = 'rUsuario')
]