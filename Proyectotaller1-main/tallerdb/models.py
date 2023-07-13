import datetime
from distutils.command.upload import upload
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
class Cliente(models.Model):
    rut              = models.CharField(primary_key=True, max_length=15)
    nombre           = models.CharField(max_length=20)
    apellido_paterno = models.CharField(max_length=20)
    apellido_materno = models.CharField(max_length=20)
    telefono         = models.CharField(max_length=45)
    email            = models.EmailField(unique=True, max_length=100, blank=True, null=True)
    direccion        = models.CharField(max_length=50, blank=True, null=True)  
    activo           = models.IntegerField()

    def __str__(self):
        return str(self.nombre)+" "+str(self.apellido_paterno)   
       
class Producto(models.Model):
    id_producto = models.CharField(primary_key=True, max_length=10,verbose_name="id_producto")
    nombre= models.CharField(max_length=50,verbose_name="Nombre") 
    imagen=models.ImageField(upload_to="imagenes",null=True,blank=True,verbose_name="Imagen")
    precio= models.IntegerField(blank=True,null=True,verbose_name="Precio")
    stock= models.IntegerField(blank=True,null=True,verbose_name="stock")

    def __str__(self):
        return self.id_producto

class Boleta(models.Model):
    id_boleta = models.AutoField(primary_key=True)
    total=models.BigIntegerField()
    fechaCompra=models.DateTimeField(blank=False,null=False,default=datetime.datetime.now)
    def _str_(self):
        return str(self.id_boleta)

class detalle_boleta(models.Model):
    id_boleta=models.ForeignKey('Boleta',blank=True,on_delete=models.CASCADE)
    id_detalle_boleta=models.AutoField(primary_key=True)
    id_pro=models.ForeignKey('Producto',on_delete=models.CASCADE)
    cantidad=models.IntegerField()
    subtotal=models.BigIntegerField()

    def _str_(self) :
        return str(self.id_detalle_boleta)