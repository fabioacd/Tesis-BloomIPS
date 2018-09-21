from datetime import date, datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Area(models.Model):
    nombre = models.CharField(max_length = 50, unique=True)
    descripcion = models.CharField(max_length = 250)

    def __str__(self):
        return self.nombre


class Empleado(AbstractUser):

    CARGOS_EMPLEADO_CHOICES = (
        ('Administrador', 'Administrador'),
        ('Coordinador', 'Coordinador'),
        ('Terapeuta', 'Terapeuta'),
        ('Secretaria', 'Secretaria'),
    )

    imagen = models.ImageField(upload_to='empleado/', default='empleado/default-image.png')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='empleados_area')  #FORANEA
    cargo = models.CharField(max_length = 20, choices=CARGOS_EMPLEADO_CHOICES)
    direccion = models.CharField(max_length = 100)
    telefono = models.CharField(max_length = 12)
    celular = models.CharField(max_length = 12)
    fecha_nacimiento = models.DateField()

    def get_cargo(self):
        return self.cargo


class Actividad(models.Model):
    nombre = models.CharField(max_length = 50)
    descripcion = models.CharField(max_length = 250)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE) #FORANEA


class Resumen(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE) #FORANEA
    paciente = models.ForeignKey('paciente.Paciente', on_delete=models.CASCADE, related_name='resumenes') #FORANEA
    fecha = models.DateField(default=date.today)
    hora = models.TimeField(default=datetime.now())
    descripcion = models.CharField(max_length = 10000)
    revisado = models.BooleanField(default=False)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='resumenes_area')  #FORANEA




class Cita(models.Model):
    class Meta:
        unique_together = (('terapeuta', 'fecha', 'hora'))
    asignador = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='asignador') #FORANEA
    terapeuta = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='terapeuta') #FORANEA
    paciente = models.ForeignKey('paciente.Paciente', on_delete=models.CASCADE) #FORANEA
    hora = models.TimeField()
    fecha = models.DateField()
    estado = models.CharField(max_length = 20)

'''
class Consolidado(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='coordinador')  # FORANEA
    paciente = models.ForeignKey('paciente.Paciente', on_delete=models.CASCADE) #FORANEA
    descripcion = models.CharField(max_length=12000)
    resumenes = models.ManyToManyField(Resumen)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
'''

class Consolidado(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='coordinador')  # FORANEA
    paciente = models.ForeignKey('paciente.Paciente', on_delete=models.CASCADE)  # FORANEA
    descripcion = models.CharField(max_length=12000)
    fecha = models.DateField()
    fecha_creacion = models.DateField(default=date.today)