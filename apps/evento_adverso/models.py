from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
from apps.empleado.models import Empleado


class ImplicadoEvento(models.Model):
    id_implicado = models.CharField(max_length=11, unique=True)  # La PK es autoincrementable
    nombre = models.CharField(max_length=50)
    seguridad_social = models.CharField(max_length=100)
    edad = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(150, message="Elije una edad válida. La edad no supera los 150 años."), MinValueValidator(1, message="Elije una edad válida. La edad no debe ser negativa.")]
     )

    def __str__(self):
        return self.nombre + ' - ' + self.id_implicado


class ClaseEventoAdverso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=250)

    def __str__(self):
        return self.nombre


class TipoEventoAdverso(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Tipo de evento")
    descripcion = models.CharField(max_length=250, )

    def __str__(self):
        return self.nombre


class EventoAdverso(models.Model):
    # El primero elemento es el que se guarda en la bd y el segundo es el que se muestra
    CLASE_EVENTO_CHOICES = (
        ('EA prevenible', 'EA prevenible'),
        ('EA NO prevenible', 'EA NO prevenible'),
        ('Incidente', 'Incidente'),
    )

    implicado = models.ForeignKey(ImplicadoEvento, on_delete=models.CASCADE)  # FORANEA
    clase_evento = models.ForeignKey(ClaseEventoAdverso, on_delete=models.CASCADE)  # FORANEA
    empleado = models.ForeignKey('empleado.Empleado', on_delete=models.CASCADE)  # FORANEA
    lugar = models.CharField(max_length=250)
    fecha_ocurrencia = models.DateField()
    fecha_reporte = models.DateField(default=date.today, blank=True)
    hora = models.TimeField()
    causa = models.CharField(max_length=500)
    acciones_realizadas = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=1000)
    tipos_evento = models.ManyToManyField(TipoEventoAdverso)
    otro_tipo_evento = models.CharField(max_length=100, blank=True)


class ProtocoloLondres(models.Model):

    evento_adverso = models.OneToOneField(EventoAdverso, on_delete=models.CASCADE, related_name='protocolo_londres',
                                          primary_key=True)  # Solo un protocolo de Londres
    fecha = models.DateField(default=date.today, blank=True)
    cronologia = models.CharField(max_length=3000)
    acciones_inseguras = models.CharField(max_length=3000)
    factores_paciente = models.CharField(max_length=2000)
    factores_tecnologia = models.CharField(max_length=2000)
    factores_individuo = models.CharField(max_length=2000)
    factores_equipo = models.CharField(max_length=2000)
    factores_ambiental = models.CharField(max_length=2000)
    factores_organizacion = models.CharField(max_length=2000)
    factores_institucional = models.CharField(max_length=2000)

    fecha_solucion = models.DateField(default=date.today, blank=True)
    actividades = models.CharField(max_length=3000)
    seguimiento = models.CharField(max_length=3000)
    responsable = models.ForeignKey('empleado.Empleado', on_delete=models.CASCADE)  # FORANEA


class SeguimientoEvento(models.Model):
    evento_adverso = models.ForeignKey(EventoAdverso, on_delete=models.CASCADE)  # FORANEA
    fecha = models.DateField(default=date.today, blank=True)
    descripcion = models.CharField(max_length=1000)
