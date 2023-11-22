from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError




# Create your models here.

class usuario(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    nombre_empresa = models.CharField(max_length=40)
    email = models.EmailField()


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatares', null=True, blank=True)
    description = models.TextField(blank=True)

class Producto(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=get_user_model()
    )
    id = models.AutoField(primary_key=True)
    bars_code = models.IntegerField(null=True, blank=True)
    nombre_producto = models.CharField(max_length=40)
    descripcion_producto = models.CharField(max_length=200)
    stock_producto = models.IntegerField()
    precio_producto = models.FloatField()
    imagen_producto = models.ImageField(upload_to='productos', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
        
    def __str__(self):
        return self.nombre_producto


class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)

    def clean(self):
        super().clean()
        if self.cantidad is not None and self.cantidad > self.producto.stock_producto:
            raise ValidationError("La cantidad excede el stock disponible del producto.")

    @property
    def valor_total(self):
        return self.producto.precio_producto * self.cantidad
    


class Posteos(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=get_user_model()
    )
    contenido = models.TextField(max_length=500)
    imagen = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)