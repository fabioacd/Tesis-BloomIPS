from datetime import date, datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from utils.utils import directorio_archivos_empleado, nombre_mes


class Area(models.Model):

    TIPO_SALUD_CHOICES = (
        ('Pos', 'POS'),
        ('No pos', 'NO POS'),
    )

    nombre = models.CharField(max_length = 50, unique=True)
    descripcion = models.CharField(max_length = 250)
    tipo = models.CharField(max_length = 20, choices=TIPO_SALUD_CHOICES)

    def __str__(self):
        return self.nombre


class Empleado(AbstractUser):

    CARGOS_EMPLEADO_CHOICES = (
        ('Administrador', 'Administrador'),
        ('Coordinador', 'Coordinador'),
        ('Terapeuta', 'Terapeuta'),
        ('Auxiliar administrativo', 'Auxiliar administrativo'),
    )

    imagen = models.ImageField(upload_to=directorio_archivos_empleado, blank=True)
    firma = models.ImageField(upload_to=directorio_archivos_empleado, blank=True)
    area = models.ManyToManyField(Area, related_name='areas_empleado')  #FORANEA
    cargo = models.CharField(max_length=30, choices=CARGOS_EMPLEADO_CHOICES)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=12, blank=True)
    celular = models.CharField(max_length=12, blank=True)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        empleado = self.username + ' - ' + self.first_name + ' ' + self.last_name
        return empleado

    def get_cargo(self):
        return self.cargo


class Actividad(models.Model):
    nombre = models.CharField(max_length = 50)
    descripcion = models.CharField(max_length = 250)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE) #FORANEA


class Resumen(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE) #FORANEA
    paciente = models.ForeignKey('paciente.Paciente', on_delete=models.CASCADE, related_name='resumenes') #FORANEA
    fecha = models.DateField()
    hora = models.TimeField()
    descripcion = models.CharField(max_length = 10000)
    revisado = models.BooleanField(default=False)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='resumenes_area')  #FORANEA

    def get_mes(self):
        mes = nombre_mes(self.fecha.strftime("%B"))
        return mes

    def get_mes_anio(self):
        mes = nombre_mes(self.fecha.strftime("%B"))
        fecha_resumen = mes + " del " + self.fecha.strftime("%Y")
        return fecha_resumen


class Cita(models.Model):
    class Meta:
        unique_together = (('terapeuta', 'fecha', 'hora'))
    asignador = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='asignador') #FORANEA
    terapeuta = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='terapeuta') #FORANEA
    paciente = models.ForeignKey('paciente.Paciente', on_delete=models.CASCADE) #FORANEA
    hora = models.TimeField()
    fecha = models.DateField()
    estado = models.CharField(max_length = 20)


class Consolidado(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='coordinador')  # FORANEA
    paciente = models.ForeignKey('paciente.Paciente', on_delete=models.CASCADE) #FORANEA
    descripcion = models.CharField(max_length=12000)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
