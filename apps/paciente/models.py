from datetime import date, datetime

from django.db import models

# Create your models here.


class Eps(models.Model):
    nit = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=12)

    def __str__(self):
        return self.nombre


class DiagnosticoCie10(models.Model):
    id_diagnostico = models.CharField(max_length=10, primary_key=True)
    descripcion = models.CharField(max_length=400)
    grupo = models.CharField(max_length=200, blank=True)

    def __str__(self):
        nombre = self.id_diagnostico + ' - ' + self.descripcion
        return nombre


class Paciente(models.Model):
    TIPOS_IDENTIFICACION_CHOICES = (
        ('Cedula ciudadania', 'Cédula ciudadania'),
        ('Tarjeta de identidad', 'Tarjeta de identidad'),
        ('Cedula de extranjeria', 'Cédula de extranjeria'),
        ('Registro civil', 'Registro civil'),
        ('Numero unico de identificacion personal', 'Número unico de identificacion personal'),
        ('Pasaporte', 'Pasaporte')
    )

    TIPOS_PACIENTE_CHOICES = (
        ('Adulto', 'Adulto'),
        ('Infante', 'Infante')
    )

    GENEROS_CHOICES = (
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino')
    )

    ESTRATOS_CHOICES = (
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06')
    )

    ESTADOS_PACIENTE_CHOICES = (
        ('Dado de alta', 'Dado de alta'),
        ('Activo', 'Activo'),
    )

    identificacion = models.CharField(max_length=11, primary_key=True)
    eps = models.ForeignKey(Eps, on_delete=models.CASCADE)  # FORANEA
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    ciudad_residencia = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    barrio = models.CharField(max_length=50)
    estrato = models.CharField(max_length=2, choices=ESTRATOS_CHOICES)
    telefono = models.CharField(max_length=10)
    celular = models.CharField(max_length=10, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    genero = models.CharField(max_length=10, choices=GENEROS_CHOICES)
    tipo_paciente = models.CharField(max_length=10, choices=TIPOS_PACIENTE_CHOICES)  # Adulto o infante
    tipo_identificacion = models.CharField(max_length=50, choices=TIPOS_IDENTIFICACION_CHOICES)
    lugar_nacimiento = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    escolaridad = models.CharField(max_length=30, blank=True)
    ocupacion = models.CharField(max_length=50, blank=True)
    motivo_consulta = models.CharField(max_length=1000)
    tiempo_evolucion = models.CharField(max_length=100, blank=True)
    remitente = models.CharField(max_length=100)
    diagnosticador = models.CharField(max_length=100)  # Especialista que diagnosticó
    ips_atencion = models.CharField(max_length=50)
    enfermedad_actual = models.CharField(max_length=1000)
    nombre_responsable = models.CharField(max_length=50)
    parentesco_responsable = models.CharField(max_length=30)
    telefono_responsable = models.CharField(max_length=15)
    evaluacion_inicial = models.CharField(max_length=1000, blank=True)
    diagnosticos_cie10 = models.ManyToManyField(DiagnosticoCie10)
    estado = models.CharField(max_length=30, choices=ESTADOS_PACIENTE_CHOICES)

    def __str__(self):
        return self.identificacion


class Familiar(models.Model):
    identificacion_familiar = models.CharField(max_length=11)  # La PK es serial.
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)  # FORANEA
    nombre = models.CharField(max_length=50)
    ocupacion = models.CharField(max_length=50)
    escolaridad = models.CharField(max_length=20)
    edad = models.IntegerField()
    relacion = models.CharField(max_length=30)  # Parentezco con el paciente


class InformacionPadres(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, primary_key=True)
    id_padre = models.CharField(max_length=11)
    id_madre = models.CharField(max_length=11)
    nombre_padre = models.CharField(max_length=50)
    nombre_madre = models.CharField(max_length=50)
    telefono_padre = models.CharField(max_length=12)
    telefono_madre = models.CharField(max_length=12)
    celular_padre = models.CharField(max_length=12)
    celular_madre = models.CharField(max_length=12)
    edad_padre = models.IntegerField()
    edad_madre = models.IntegerField()


class Entrada(models.Model):
    empleado = models.ForeignKey('empleado.Empleado', on_delete=models.CASCADE)  # FORANEA
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)  # FORANEA
    fecha = models.DateField(default=date.today)
    hora = models.TimeField(default=datetime.now())
    descripcion = models.CharField(max_length=3000)
