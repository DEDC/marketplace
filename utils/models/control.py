# Python
import uuid
# Django
from django.db import models

class ControlInfo(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4, editable = False)
    fecha_reg = models.DateTimeField(auto_now_add = True)
    fecha_mod = models.DateTimeField(auto_now = True)
    activo = models.BooleanField(default = True, editable = False)

    class Meta:
        abstract = True

def path_image(instance, filename):
    extfile = filename.split('.')[-1]
    return 'image/products/{}/img-{}.{}'.format(instance.uuid, str(instance.uuid)[:8], extfile)