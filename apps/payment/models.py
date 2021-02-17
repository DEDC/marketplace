# Django
from django.db import models
# app users
from apps.users.models import Usuarios
# utils
from utils.models.control import ControlInfo

class Customers(ControlInfo):
    identifier = 'CUS'
    extra = '17'
    id_customer = models.CharField(max_length = 50, editable = False)
    user = models.OneToOneField(Usuarios, related_name = 'customer_payment', on_delete = models.PROTECT, editable = False)