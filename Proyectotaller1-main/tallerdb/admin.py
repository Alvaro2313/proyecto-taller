from django.contrib import admin
from .models import Cliente,Producto,Boleta,detalle_boleta
# Register your models here.
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Boleta)
admin.site.register(detalle_boleta)