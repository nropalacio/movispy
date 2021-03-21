from django.contrib import admin
from .models import Pelicula, Cine, Funcion, Dia, Sucursal

#admin.site.register(Pelicula)
admin.site.register(Cine)
admin.site.register(Funcion)
admin.site.register(Sucursal)
admin.site.register(Dia)