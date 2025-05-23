# Generated by Django 2.2.4 on 2021-03-02 20:03

import django.core.validators
from django.db import migrations, models
import utils.models.control
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Envios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('folio', models.CharField(editable=False, max_length=25, null=True, unique=True)),
                ('fecha_reg', models.DateTimeField(auto_now_add=True)),
                ('fecha_mod', models.DateTimeField(auto_now=True)),
                ('activo', models.BooleanField(default=True, editable=False)),
                ('estatus', models.CharField(choices=[('preparando', 'Preparando'), ('enviado', 'Enviado'), ('entregado', 'Entregado')], default='preparando', max_length=50)),
                ('direccion_txt', models.TextField(editable=False, null=True)),
            ],
            options={
                'ordering': ['-fecha_reg'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Imagenes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('fecha_reg', models.DateTimeField(auto_now_add=True)),
                ('fecha_mod', models.DateTimeField(auto_now=True)),
                ('activo', models.BooleanField(default=True, editable=False)),
                ('imagen', models.ImageField(upload_to=utils.models.control.path_image)),
            ],
            options={
                'ordering': ['-fecha_reg'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('folio', models.CharField(editable=False, max_length=25, null=True, unique=True)),
                ('fecha_reg', models.DateTimeField(auto_now_add=True)),
                ('fecha_mod', models.DateTimeField(auto_now=True)),
                ('activo', models.BooleanField(default=True, editable=False)),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre del producto')),
                ('slug', models.SlugField(blank=True, editable=False)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(10000000.0)], verbose_name='Precio unitario')),
                ('cantidad', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100000)], verbose_name='Cantidad disponible')),
                ('descripcion', models.CharField(max_length=200, verbose_name='Descripción del producto')),
                ('comision', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(10000000.0)], verbose_name='Comisión del producto')),
                ('tipo_comision', models.CharField(choices=[('directa', 'Por monto directo'), ('porcentaje', 'Por porcentaje')], max_length=50, null=True, verbose_name='Tipo de comisión')),
                ('imagen', models.ImageField(upload_to=utils.models.control.path_image, verbose_name='Imagen principal')),
            ],
            options={
                'ordering': ['-fecha_reg'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Productos_Ventas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_reg', models.DateTimeField(auto_now_add=True)),
                ('fecha_mod', models.DateTimeField(auto_now=True)),
                ('activo', models.BooleanField(default=True, editable=False)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(10000000.0)])),
                ('cantidad', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100000)])),
            ],
            options={
                'ordering': ['-fecha_reg'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ventas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('folio', models.CharField(editable=False, max_length=25, null=True, unique=True)),
                ('fecha_reg', models.DateTimeField(auto_now_add=True)),
                ('fecha_mod', models.DateTimeField(auto_now=True)),
                ('activo', models.BooleanField(default=True, editable=False)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(10000000.0)])),
                ('id_payment', models.CharField(editable=False, max_length=50, null=True)),
                ('productos', models.ManyToManyField(through='mkt.Productos_Ventas', to='mkt.Productos')),
            ],
            options={
                'ordering': ['-fecha_reg'],
            },
        ),
    ]
