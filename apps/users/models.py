from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuarios(AbstractUser):
    class Meta:
        ordering = ['-is_superuser', 'date_joined']
    username = models.CharField('Nombre de usuario', max_length = 100, null = True, blank = True)
    email = models.EmailField('Correo electrónico', unique = True)
    phone_number = models.CharField('Número de teléfono', max_length = 10, unique = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name', 'username']