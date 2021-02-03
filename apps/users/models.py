# django
from django.db import models
from django.contrib.auth.models import AbstractUser
# utils
from utils.models.control import ControlInfo

class Usuarios(AbstractUser):
    class Meta:
        ordering = ['-is_superuser', 'date_joined']
    username = models.CharField('Nombre de usuario', max_length = 100, null = True, blank = True)
    email = models.EmailField('Correo electrónico', unique = True)
    phone_number = models.CharField('Número de teléfono', max_length = 10, unique = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name', 'username']

class Direcciones(ControlInfo):
    uuid = None
    calle = models.CharField('Nombre de la calle', max_length = 100)
    no_calle = models.CharField('Número exterior', max_length = 6, default = 's/n')
    no_interior = models.CharField('Número interior', max_length = 6, default = 's/n')
    colonia = models.CharField('Nombre de la colonia', max_length = 100)
    referencias = models.CharField('Referencias para ubicar el lugar', max_length = 200)
    instrucciones = models.CharField('Instrucciones de entrega', max_length = 200)
    usuario = models.ForeignKey(Usuarios, on_delete = models.CASCADE, related_name = 'direcciones', editable = False)