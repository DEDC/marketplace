# django
from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
# utils
from utils.models.control import ControlInfo, path_image


class Productos(ControlInfo):
    identifier = 'CT'
    nombre = models.CharField('Nombre del producto', max_length = 50)
    slug = models.SlugField(editable = False, blank = True)
    precio = models.DecimalField('Precio unitario', max_digits = 10, decimal_places = 2, validators = [MinValueValidator(1.00), MaxValueValidator(10000000.00)])
    cantidad = models.PositiveIntegerField('Cantidad disponible', validators = [MaxValueValidator(100000)])
    descripcion = models.CharField('Descripción del producto', max_length = 200)
    comision = models.DecimalField('Comisión del producto', max_digits = 10, decimal_places = 2, validators = [MinValueValidator(1.00), MaxValueValidator(10000000.00)], null = True)
    tipo_comision = models.CharField('Tipo de comisión', max_length = 50, choices = [('directa', 'Por monto directo'), ('porcentaje', 'Por porcentaje')], null = True)
    imagen = models.ImageField('Imagen principal', upload_to = path_image)

    def get_public_price(self):
        price = 0
        if self.tipo_comision == 'directa':
            price = self.precio + self.comision
        else:
            price = self.precio +  round((self.precio * self.comision) / 100)
        return price
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Productos, self).save(*args, **kwargs)

class Imagenes(ControlInfo):
    folio = None
    imagen = models.ImageField(upload_to = path_image)
    producto = models.ForeignKey(Productos, related_name = 'imagenes', on_delete = models.CASCADE)

class Ventas(ControlInfo):
    identifier = 'CT-VT'
    total = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(1.00), MaxValueValidator(10000000.00)])
    productos = models.ManyToManyField(Productos, through = 'Productos_Ventas')

class Productos_Ventas(ControlInfo):
    uuid = None
    folio = None
    producto = models.ForeignKey(Productos, on_delete = models.CASCADE)
    venta = models.ForeignKey(Ventas, on_delete = models.CASCADE)
    precio = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(1.00), MaxValueValidator(10000000.00)])
    cantidad = models.PositiveIntegerField(validators = [MaxValueValidator(100000)])

class Envios(ControlInfo):
    identifier = 'CT-EV'
    status_choices = (('preparando', 'Preparando'), ('enviado', 'Enviado'), ('entregado', 'Entregado'))
    venta = models.ForeignKey(Ventas, related_name = 'envio', on_delete = models.CASCADE)
    estatus = models.CharField(max_length = 50, choices = status_choices, default = 'preparando')