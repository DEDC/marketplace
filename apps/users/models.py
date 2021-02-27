# django
from django.db import models
from django.contrib.auth.models import AbstractUser
from .mixins.email_confirmation import EmailConfirmation
from django.conf import settings
from django.core.validators import RegexValidator
# utils
from utils.models.control import ControlInfo

class Usuarios(EmailConfirmation, AbstractUser):
    html_confirmation_content = 'mail/users/account_confirmation.html'
    text_confirmation_content = 'mail/users/account_confirmation.txt'
    from_ = settings.DEFAULT_FROM_EMAIL
    class Meta:
        ordering = ['-is_superuser', 'date_joined']
    username = models.CharField('Nombre de usuario', max_length = 100, null = True, blank = True)
    email = models.EmailField('Correo electrónico', unique = True)
    phone_number = models.CharField('Número de teléfono', max_length = 10, validators = [RegexValidator('^[0-9]*$', 'Ingrese un número de telefono correcto')])
    is_confirmed = models.BooleanField(default = False, editable = False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name', 'username']

class Direcciones(ControlInfo):
    folio = None
    alias = models.CharField('Alias de la dirección', max_length = 100, null = True)
    calle = models.CharField('Nombre de la calle', max_length = 100)
    no_calle = models.CharField('Número exterior', max_length = 6, default = 's/n')
    no_interior = models.CharField('Número interior', max_length = 6, default = 's/n')
    colonia = models.CharField('Nombre de la colonia', max_length = 100)
    codigo_postal = models.CharField('Código postal', max_length = 5, null = True)
    referencias = models.CharField('Referencias para ubicar el lugar', max_length = 200)
    instrucciones = models.CharField('Instrucciones de entrega', max_length = 200)
    default = models.BooleanField('Usar esta dirección como predeterminada', default = False)
    usuario = models.ForeignKey(Usuarios, on_delete = models.CASCADE, related_name = 'direcciones', editable = False)