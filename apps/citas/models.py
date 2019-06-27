from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class Cita(models.Model):
    class Meta:
        unique_together = (('terapeuta', 'fecha', 'hora'))
    asignador = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='asignador') #FORANEA
    terapeuta = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='terapeuta') #FORANEA
    paciente = models.ForeignKey('paciente.Paciente', on_delete=models.CASCADE) #FORANEA
    hora = models.TimeField()
    fecha = models.DateField()
    estado = models.CharField(max_length = 20)