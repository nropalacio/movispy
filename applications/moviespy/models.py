from django.db import models
from django.utils import timezone
from datetime import datetime


# Create your models here.
class Pelicula(models.Model):
    titulo = models.CharField(max_length=100)
    activo = models.BooleanField()

    def __str__(self):
        return self.titulo

class Cine(models.Model):
    nombre = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    activo = models.BooleanField()

    def __str__(self):
        return self.nombre

class Dia(models.Model):
    dia = models.DateField()
    activo = models.BooleanField()


class Sucursal(models.Model):
    nombre = models.CharField(max_length=50)
    cine = models.ForeignKey(Cine, on_delete=models.CASCADE)
    activo = models.BooleanField()

    def __str__(self):
        return self.nombre

class Funcion(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    fecha = models.ForeignKey(Dia, on_delete=models.CASCADE)
    pelicula = models.CharField(max_length=100)
    url_pelicula = models.CharField(max_length=100)
    tipo_funcion = models.CharField(max_length=30)
    hora = models.CharField(max_length=6)
    sala = models.CharField(max_length=10)
    asientos = models.IntegerField(default=0)
    num_func = models.IntegerField(default=0)
    num_hors = models.IntegerField(default=0)
    activo = models.BooleanField()

    def __str__(self):
        return str(self.id) + ' ' + self.pelicula + ' ' + self.sucursal.nombre + ' ' + self.tipo_funcion + ' ' + self.hora + ' ' + self.sala + ' ' + str(self.asientos)



