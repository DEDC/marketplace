# Python
import uuid
# Django
from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator

def path_image(instance, filename):
    extfile = filename.split('.')[-1]
    return 'image/products/{}/img-{}.{}'.format(instance.uuid, str(instance.uuid)[:8], extfile)

class Productos(models.Model):
    nombre = models.CharField('Nombre del producto', max_length = 50)
    slug = models.SlugField(editable = False, blank = True)
    uuid = models.UUIDField(default = uuid.uuid4, editable = False, blank = True)
    precio = models.DecimalField('Precio unitario', max_digits = 10, decimal_places = 2, validators = [MinValueValidator(1.00), MaxValueValidator(10000000.00)])
    cantidad = models.PositiveIntegerField('Cantidad disponible', validators = [MaxValueValidator(100000)])
    descripcion = models.CharField('Descripción del producto', max_length = 200)
    imagen = models.ImageField('Imagen principal', upload_to = path_image)
    fecha_reg = models.DateTimeField(auto_now_add = True, null = True)
    fecha_mod = models.DateTimeField(auto_now = True, null = True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Productos, self).save(*args, **kwargs)

class Imagenes(models.Model):
    imagen = models.ImageField(upload_to = path_image)
    fecha_reg = models.DateTimeField(auto_now_add = True)
    producto = models.ForeignKey(Productos, related_name = 'imagenes', on_delete = models.CASCADE)

class Ventas(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4, editable = False, blank = True)
    total = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(1.00), MaxValueValidator(10000000.00)])
    productos = models.ManyToManyField(Productos, through = 'Productos_Ventas')
    fecha_reg = models.DateTimeField(auto_now_add = True)
    fecha_mod = models.DateTimeField(auto_now = True)

class Productos_Ventas(models.Model):
    producto = models.ForeignKey(Productos, on_delete = models.CASCADE)
    venta = models.ForeignKey(Ventas, on_delete = models.CASCADE)
    precio = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(1.00), MaxValueValidator(10000000.00)])
    cantidad = models.PositiveIntegerField(validators = [MaxValueValidator(100000)])
    fecha_reg = models.DateTimeField(auto_now_add = True)
    fecha_mod = models.DateTimeField(auto_now = True)

class Envios(models.Model):
    status_choices = (('preparando', 'Preparando'), ('enviado', 'Enviado'), ('entregado', 'Entregado'))
    uuid = models.UUIDField(default = uuid.uuid4, editable = False, blank = True)
    venta = models.ForeignKey(Ventas, related_name = 'envio', on_delete = models.CASCADE)
    estatus = models.CharField(max_length = 50, choices = status_choices, default = 'preparando')
    fecha_reg = models.DateTimeField(auto_now_add = True)
    fecha_mod = models.DateTimeField(auto_now = True)