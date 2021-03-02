# Python
import uuid
# Django
from django.db import models

class ControlInfo(models.Model):
    identifier = ''
    extra = '17'
    uuid = models.UUIDField(default = uuid.uuid4, editable = False, unique = True)
    folio = models.CharField(max_length = 25, unique = True, null = True, editable = False)
    fecha_reg = models.DateTimeField(auto_now_add = True)
    fecha_mod = models.DateTimeField(auto_now = True)
    activo = models.BooleanField(default = True, editable = False)

    def save(self, *args, **kwargs):
        self.identifier = '{}-{}-{}'.format(self.identifier, str(self.uuid).upper()[:8], self.extra)
        self.folio = self.identifier
        super(ControlInfo, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-fecha_reg']
        abstract = True

def path_image(instance, filename):
    extfile = filename.split('.')[-1]
    return 'images/products/{}/img-{}.{}'.format(instance.uuid, str(instance.uuid)[:8], extfile)