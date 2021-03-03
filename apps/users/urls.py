# Django
from django.urls import path
# app users
from .views import vLogin, vLogout, vRegistro, vConfirmUser, vDirecciones, ListOrders, vResetPasswordEmail, PasswordResetEmailConfirm

app_name = 'user'

urlpatterns = [
    path('login/', vLogin, name = 'login'),
    path('logout/', vLogout, name = 'logout'),
    path('registro/', vRegistro, name = 'rUsuario'),
    path('activate/<slug:uidb64>/<slug:token>)/', vConfirmUser, name = 'confirm_user'),
    path('agregar/direccion', vDirecciones, name = 'rDirecciones'),
    path('pedidos/', ListOrders.as_view(), name = 'list_orders'),
    path('reset-password', vResetPasswordEmail, name = 'reset_password'),
    path('reset_password_confirm/<uidb64>/<token>', PasswordResetEmailConfirm, name='reset_password_confirm'),
]