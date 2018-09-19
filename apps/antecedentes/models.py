from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


class AntecedentesPersonales(models.Model):
    paciente = models.OneToOneField('paciente.Paciente', on_delete=models.CASCADE, primary_key=True)
    farmacologicos = models.CharField(max_length=1000)
    alergicos = models.CharField(max_length=1000, blank=True)
    patologicos = models.CharField(max_length=1000)
    toxicos = models.CharField(max_length=1000, blank=True)
    quirurgicos = models.CharField(max_length=1000)
    prescripcion_medica = models.CharField(max_length=1000)
    esquema_vacunacion = models.CharField(max_length=1000, blank=True)


class TipoVivienda(models.Model):
    tipo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=250)

    def __str__(self):
        return self.tipo
    '''Propia
        Alquiler
        Familiar
        Otro
    '''


class AntecedentesPsicosociales(models.Model):
    TOTAL_INGRESOS_CHOICES = (
        ('Menos de un SMLV', 'Menos de un SMLV'),
        ('Entre 1 y 2 SMLV', 'Entre 1 y 2 SMLV'),
        ('Entre 3 y 5 SMLV', 'Entre 3 y 5 SMLV'),
        ('Más de 5 SMLV', 'Más de 5 SMLV')
    )

    SECTOR_VIVIENDA_CHOICES = (
        ('Rural', 'Rural'),
        ('Urbano', 'Urbano')
    )

    paciente = models.OneToOneField('paciente.Paciente', on_delete=models.CASCADE, primary_key=True)
    numero_habitantes = models.PositiveIntegerField()
    num_integrantes_laboran = models.PositiveIntegerField()
    lugar_entre_hermanos = models.CharField(max_length=50)
    num_hermanos = models.IntegerField()
    gmfcs = models.CharField(max_length=100)
    observaciones_vivienda = models.CharField(max_length=1000, blank=True)
    observacion_servicios = models.CharField(max_length=1000, blank=True)
    total_ingresos = models.CharField(max_length=20, choices=TOTAL_INGRESOS_CHOICES)
    tipo_vivienda = models.ForeignKey(TipoVivienda, on_delete=models.CASCADE)  # FORANEA
    otro_tipo_vivienda = models.CharField(max_length=30, blank=True)
    sector_vivienda = models.CharField(max_length=10, choices=SECTOR_VIVIENDA_CHOICES)
    gas = models.BooleanField()
    internet = models.BooleanField()
    agua = models.BooleanField()
    energia = models.BooleanField()


class TipoConsumo(models.Model):
    tipo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=250)

    def __str__(self):
        return self.tipo
    '''Alcohol
        Tabaco
        Otro
    '''


class AntecedentesGestacionales(models.Model):
    paciente = models.OneToOneField('paciente.Paciente', on_delete=models.CASCADE, primary_key=True)
    planeado = models.BooleanField()
    deseado = models.BooleanField()
    gemelar = models.BooleanField()
    controlado = models.BooleanField()
    consumo_embarazo = models.ForeignKey(TipoConsumo, on_delete=models.CASCADE)  # FORANEA
    otro_consumo = models.CharField(max_length=50, blank=True)
    semanas_gestacion = models.PositiveIntegerField()
    parto_termino = models.BooleanField()
    parto_prematuro = models.BooleanField()
    amenaza_aborto = models.BooleanField()
    trabajo_parto_prolongado = models.BooleanField()
    meconio = models.BooleanField()
    diabetes = models.BooleanField()
    otro_sintoma = models.CharField(max_length=50, blank=True)
    circular_cordon = models.BooleanField()
    placenta_previa = models.BooleanField()
    torchs = models.BooleanField()
    cesarea = models.BooleanField()
    preeclamsia = models.BooleanField()
    forceps = models.BooleanField()


class AntecedentesFamiliares(models.Model):
    paciente = models.OneToOneField('paciente.Paciente', on_delete=models.CASCADE, primary_key=True)
    enfermedad_madre = models.CharField(max_length=1000)
    enfermedad_padre = models.CharField(max_length=1000)
    enfermedad_hermanos = models.CharField(max_length=1000)
    otros_antecedentes = models.CharField(max_length=1000)
    antecedentes_clinicos = models.CharField(max_length=1000)
