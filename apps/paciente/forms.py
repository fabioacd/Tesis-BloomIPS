from datetime import datetime
import magic
from django.core.validators import FileExtensionValidator
from django import forms
from django_select2.forms import Select2MultipleWidget, Select2Widget
from django.forms import SelectDateWidget, BaseFormSet
from .models import Paciente, DiagnosticoCie10, Entrada, ArchivosPaciente

from apps.empleado.models import Area

class AgregarArchivosForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AgregarArchivosForm, self).__init__(*args, **kwargs)
        self.fields['archivo'].required = True
        self.fields['descripcion'].required = True
        self.fields['paciente'].queryset = Paciente.objects.filter(estado='Activo')

        # Placeholders
        self.fields['descripcion'].widget.attrs['placeholder'] = "Ej. Paciente al ingresar a la IPS - 20/17/19"

    def clean(self):
        form_data = super().clean()

        if form_data.get('archivo'):
            archivo = form_data.get('archivo').read(1048576)
            if magic.from_buffer(archivo, mime=True) != 'image/png':
                if magic.from_buffer(archivo, mime=True) != 'image/jpeg':
                    if magic.from_buffer(archivo, mime=True) != 'application/pdf':
                        self.add_error("archivo", "Únicamente se admiten archivos de tipo 'jpg', 'png' o 'pdf'")
            else:
                pass

        return form_data

    class Meta:
        model = ArchivosPaciente
        fields = ('archivo', 'paciente', 'descripcion')
        labels = {
            'archivo': "Agregar archivo",
            'descripcion': "Descripción",
            'paciente': "Seleccione paciente"
        }
        widgets = {
            'paciente': Select2Widget(),
            "descripcion": forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
        }

class RegistrarPacienteForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", widget=forms.SelectDateWidget())

    def __init__(self, *args, **kwargs):
        super(RegistrarPacienteForm, self).__init__(*args, **kwargs)
        if self.is_bound:
            self.fields['diagnosticos_cie10'].queryset = DiagnosticoCie10.objects.all()
        else:
            self.fields['diagnosticos_cie10'].queryset = DiagnosticoCie10.objects.none()
        self.fields['tipo_paciente'].widget.attrs['id'] = "tipo_paciente"
        self.fields['nombre_responsable'].required = False
        self.fields['parentesco_responsable'].required = False
        self.fields['telefono_responsable'].required = False
        self.fields['evaluacion_inicial'].required = False
        self.fields['tiempo_evolucion'].required = False
        self.fields['email'].required = False
        self.fields['fecha_nacimiento'].widget = SelectDateWidget(years=range(1940, datetime.now().year + 1))
        self.fields['nombre'].widget.attrs['class'] = "alphabetic"
        self.fields['nombre_responsable'].widget.attrs['class'] = "alphabetic"
        self.fields['parentesco_responsable'].widget.attrs['class'] = "alphabetic"
        self.fields['ocupacion'].widget.attrs['class'] = "alphabetic"
        self.fields['remitente'].widget.attrs['class'] = "alphabetic"
        self.fields['diagnosticador'].widget.attrs['class'] = "alphabetic"
        self.fields['apellido'].widget.attrs['class'] = "alphabetic"
        self.fields['lugar_nacimiento'].widget.attrs['class'] = "locations"
        self.fields['ciudad_residencia'].widget.attrs['class'] = "locations"
        self.fields['escolaridad'].widget.attrs['class'] = "alphabetic"
        self.fields['barrio'].widget.attrs['class'] = "locations"
        self.fields['telefono'].widget.attrs['class'] = "numeric"
        self.fields['celular'].widget.attrs['class'] = "numeric"
        self.fields['identificacion'].widget.attrs['class'] = "numeric"
        self.fields['telefono_responsable'].widget.attrs['class'] = "numeric"

        # Placeholders
        self.fields['identificacion'].widget.attrs['placeholder'] = "Ej. 1144958632"
        self.fields['nombre'].widget.attrs['placeholder'] = "Ej. Luis Felipe"
        self.fields['apellido'].widget.attrs['placeholder'] = "Ej. Gómez Castrillon"
        self.fields['lugar_nacimiento'].widget.attrs['placeholder'] = "Ej. Cali, Valle del Cauca"
        self.fields['ciudad_residencia'].widget.attrs['placeholder'] = "Ej. Medellín, Antioquia"
        self.fields['direccion'].widget.attrs['placeholder'] = "Ej. Calle 5 Sur #302"
        self.fields['barrio'].widget.attrs['placeholder'] = "Ej. El poblado"
        self.fields['telefono'].widget.attrs['placeholder'] = "Ej. 4190028"
        self.fields['celular'].widget.attrs['placeholder'] = "Ej. 3214567894"
        self.fields['escolaridad'].widget.attrs['placeholder'] = "Ej. Profesional"
        self.fields['email'].widget.attrs['placeholder'] = "Ej. luis.univalle@gmail.com"

    def clean(self):
        form_data = super().clean()

        if form_data.get('evaluacion_inicial'):
            ev_inicial = form_data.get('evaluacion_inicial').read(1048576)
            if magic.from_buffer(ev_inicial, mime=True) != 'application/pdf':
                self.add_error("evaluacion_inicial", "Únicamente se admiten archivos de tipo 'pdf'")
            else:
                pass

        return form_data

    class Meta:
        model = Paciente
        fields = ('identificacion', 'eps', 'nombre', 'apellido', 'ciudad_residencia', 'direccion', 'barrio',
                  'estrato', 'telefono', 'celular', 'email', 'genero', 'tipo_paciente', 'tipo_identificacion',
                  'lugar_nacimiento', 'fecha_nacimiento', 'escolaridad', 'ocupacion', 'motivo_consulta',
                  'tiempo_evolucion', 'remitente', 'diagnosticador', 'ips_atencion', 'enfermedad_actual',
                  'nombre_responsable', 'parentesco_responsable', 'telefono_responsable', 'evaluacion_inicial',
                  'diagnosticos_cie10')
        labels = {
            'tipo_paciente': "Tipo de paciente",
            'tipo_identificacion': "Tipo de identificación",
            'identificacion': "Número de identificación",
            'ciudad_residencia': "Ciudad de residencia",
            'direccion': "Dirección",
            'telefono': "Teléfono",
            'genero': "Género",
            'lugar_nacimiento': "Lugar de nacimiento",
            'motivo_consulta': "Motivo de la consulta",
            'tiempo_evolucion': "Tiempo de evolución",
            'ips_atencion': "IPS de atención primaria",
            'eps': "EPS",
            'nombre_responsable': "Nombre del responsable",
            'parentesco_responsable': "Parentesco del responsable",
            'telefono_responsable': "Teléfono del responsable",
            'evaluacion_inicial': "Evaluación inicial",
            'diagnosticos_cie10': "Diagnósticos cie10",
            'nombre': "Nombre(s)",
            'apellido': "Apellidos",
            'remitente': "Remitido por",
            'diagnosticador': "Especialista que diagnostica",
            'ocupacion': "Ocupación",
            'escolaridad': "Grado de escolaridad",
            'enfermedad_actual': "Diagnóstico actual"
        }
        widgets = {
            "enfermedad_actual": forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            "motivo_consulta": forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            "evaluacion_inicial": forms.widgets.FileInput(attrs={'class': 'dropify', 'data-height': 150}),
            "diagnosticos_cie10": Select2MultipleWidget
        }

class VerPacienteForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", widget=forms.SelectDateWidget())

    def __init__(self, *args, **kwargs):
        super(VerPacienteForm, self).__init__(*args, **kwargs)
        paciente = self.instance
        if paciente:
            self.fields['diagnosticos_cie10'].queryset = DiagnosticoCie10.objects.filter(diagnosticos_paciente=paciente)
        else:
            self.fields['diagnosticos_cie10'].queryset = DiagnosticoCie10.objects.none()
        self.fields['tipo_paciente'].widget.attrs['disabled'] = "disabled"
        self.fields['eps'].widget.attrs['disabled'] = "disabled"
        self.fields['nombre'].widget.attrs['readonly'] = "readonly"
        self.fields['apellido'].widget.attrs['readonly'] = "readonly"
        self.fields['ciudad_residencia'].widget.attrs['readonly'] = "readonly"
        self.fields['direccion'].widget.attrs['readonly'] = "readonly"
        self.fields['barrio'].widget.attrs['readonly'] = "readonly"
        self.fields['estrato'].widget.attrs['disabled'] = "disabled"
        self.fields['identificacion'].widget.attrs['readonly'] = "readonly"
        self.fields['telefono'].widget.attrs['readonly'] = "readonly"
        self.fields['celular'].widget.attrs['readonly'] = "readonly"
        self.fields['email'].widget.attrs['readonly'] = "readonly"
        self.fields['genero'].widget.attrs['disabled'] = "disabled"
        self.fields['tipo_identificacion'].widget.attrs['disabled'] = "disabled"
        self.fields['lugar_nacimiento'].widget.attrs['readonly'] = "readonly"
        self.fields['fecha_nacimiento'].widget = SelectDateWidget(years=range(1940, datetime.now().year + 1))
        self.fields['fecha_nacimiento'].widget.attrs['disabled'] = "disabled"
        self.fields['escolaridad'].widget.attrs['readonly'] = "readonly"
        self.fields['ocupacion'].widget.attrs['readonly'] = "readonly"
        self.fields['motivo_consulta'].widget.attrs['readonly'] = "readonly"
        self.fields['tiempo_evolucion'].widget.attrs['readonly'] = "readonly"
        self.fields['remitente'].widget.attrs['readonly'] = "readonly"
        self.fields['diagnosticador'].widget.attrs['readonly'] = "readonly"
        self.fields['ips_atencion'].widget.attrs['readonly'] = "readonly"
        self.fields['enfermedad_actual'].widget.attrs['readonly'] = "readonly"
        self.fields['nombre_responsable'].widget.attrs['readonly'] = "readonly"
        self.fields['parentesco_responsable'].widget.attrs['readonly'] = "readonly"
        self.fields['telefono_responsable'].widget.attrs['readonly'] = "readonly"
        self.fields['evaluacion_inicial'].widget.attrs['disabled'] = "disabled"
        self.fields['diagnosticos_cie10'].widget.attrs['disabled'] = "disabled"
        self.fields['estado'].widget.attrs['disabled'] = "disabled"
        self.fields['diagnosticos_cie10'].label = "Diagnósticos cie10"

    class Meta:
        model = Paciente
        fields = ('identificacion', 'eps', 'nombre', 'apellido', 'ciudad_residencia', 'direccion', 'barrio',
                  'estrato', 'telefono', 'celular', 'email', 'genero', 'tipo_paciente', 'tipo_identificacion',
                  'lugar_nacimiento', 'fecha_nacimiento', 'escolaridad', 'ocupacion', 'motivo_consulta',
                  'tiempo_evolucion', 'remitente', 'diagnosticador', 'ips_atencion', 'enfermedad_actual',
                  'nombre_responsable', 'parentesco_responsable', 'telefono_responsable', 'evaluacion_inicial',
                  'diagnosticos_cie10', 'estado')
        labels = {
            'tipo_paciente': "Tipo de paciente",
            'tipo_identificacion': "Tipo de identificación",
            'identificacion': "Número de identificación",
            'ciudad_residencia': "Ciudad de residencia",
            'direccion': "Dirección",
            'telefono': "Teléfono",
            'genero': "Género",
            'lugar_nacimiento': "Lugar de nacimiento",
            'motivo_consulta': "Motivo de la consulta",
            'tiempo_evolucion': "Tiempo de evolución",
            'ips_atencion': "IPS de atención primaria",
            'eps': "EPS",
            'nombre_responsable': "Nombre del responsable",
            'parentesco_responsable': "Parentesco del responsable",
            'telefono_responsable': "Teléfono del responsable",
            'evaluacion_inicial': "Evaluación inicial",
            'diagnosticos_cie10': "Diagnósticos cie10",
            'nombre': "Nombre(s)",
            'apellido': "Apellidos",
            'remitente': "Remitido por",
            'diagnosticador': "Especialista que diagnostica",
            'ocupacion': "Ocupación",
            'escolaridad': "Grado de escolaridad",

        }
        widgets = {
            "enfermedad_actual": forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            "motivo_consulta": forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            "diagnosticos_cie10": Select2MultipleWidget()
        }

class ModificarPacienteForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", widget=forms.SelectDateWidget())

    def __init__(self, *args, **kwargs):
        super(ModificarPacienteForm, self).__init__(*args, **kwargs)
        paciente = self.instance
        if paciente:
            if self.is_bound:
                self.fields['diagnosticos_cie10'].queryset = DiagnosticoCie10.objects.all()
            else:
                self.fields['diagnosticos_cie10'].queryset = DiagnosticoCie10.objects.filter(diagnosticos_paciente=paciente)
        else:
            self.fields['diagnosticos_cie10'].queryset = DiagnosticoCie10.objects.none()

        self.fields['fecha_nacimiento'].widget = SelectDateWidget(years=range(1940, datetime.now().year + 1))
        self.fields['identificacion'].widget.attrs['readonly'] = "readonly"
        self.fields['tipo_identificacion'].widget.attrs['disabled'] = "disabled"
        self.fields['tipo_paciente'].widget.attrs['disabled'] = "disabled"
        self.fields['nombre_responsable'].required = False
        self.fields['parentesco_responsable'].required = False
        self.fields['telefono_responsable'].required = False
        self.fields['evaluacion_inicial'].required = False
        self.fields['email'].required = False
        self.fields['nombre'].widget.attrs['class'] = "alphabetic"
        self.fields['nombre_responsable'].widget.attrs['class'] = "alphabetic"
        self.fields['parentesco_responsable'].widget.attrs['class'] = "alphabetic"
        self.fields['ocupacion'].widget.attrs['class'] = "alphabetic"
        self.fields['remitente'].widget.attrs['class'] = "alphabetic"
        self.fields['diagnosticador'].widget.attrs['class'] = "alphabetic"
        self.fields['apellido'].widget.attrs['class'] = "alphabetic"
        self.fields['lugar_nacimiento'].widget.attrs['class'] = "locations"
        self.fields['ciudad_residencia'].widget.attrs['class'] = "locations"
        self.fields['escolaridad'].widget.attrs['class'] = "alphabetic"
        self.fields['barrio'].widget.attrs['class'] = "locations"
        self.fields['telefono'].widget.attrs['class'] = "numeric"
        self.fields['celular'].widget.attrs['class'] = "numeric"
        self.fields['identificacion'].widget.attrs['class'] = "numeric"
        self.fields['telefono_responsable'].widget.attrs['class'] = "numeric"

        # Placeholders
        self.fields['identificacion'].widget.attrs['placeholder'] = "Ej. 1144958632"
        self.fields['nombre'].widget.attrs['placeholder'] = "Ej. Luis Felipe"
        self.fields['apellido'].widget.attrs['placeholder'] = "Ej. Gómez Castrillon"
        self.fields['lugar_nacimiento'].widget.attrs['placeholder'] = "Ej. Cali, Valle del Cauca"
        self.fields['ciudad_residencia'].widget.attrs['placeholder'] = "Ej. Medellín, Antioquia"
        self.fields['direccion'].widget.attrs['placeholder'] = "Ej. Calle 5 Sur #302"
        self.fields['barrio'].widget.attrs['placeholder'] = "Ej. El poblado"
        self.fields['telefono'].widget.attrs['placeholder'] = "Ej. 4190028"
        self.fields['celular'].widget.attrs['placeholder'] = "Ej. 3214567894"
        self.fields['escolaridad'].widget.attrs['placeholder'] = "Ej. Profesional"
        self.fields['email'].widget.attrs['placeholder'] = "Ej. luis.univalle@gmail.com"

    def clean(self):
        form_data = super().clean()

        if form_data.get('evaluacion_inicial'):
            ev_inicial = form_data.get('evaluacion_inicial').read(1048576)
            if magic.from_buffer(ev_inicial, mime=True) != 'application/pdf':
                self.add_error("evaluacion_inicial", "Únicamente se admiten archivos de tipo 'pdf'")
            else:
                pass
        return form_data

    class Meta:
        model = Paciente
        fields = ('identificacion', 'eps', 'nombre', 'apellido', 'ciudad_residencia', 'direccion', 'barrio',
                  'estrato', 'telefono', 'celular', 'email', 'genero', 'tipo_paciente', 'tipo_identificacion',
                  'lugar_nacimiento', 'fecha_nacimiento', 'escolaridad', 'ocupacion', 'motivo_consulta',
                  'tiempo_evolucion', 'remitente', 'diagnosticador', 'ips_atencion', 'enfermedad_actual',
                  'nombre_responsable', 'parentesco_responsable', 'telefono_responsable', 'evaluacion_inicial',
                  'diagnosticos_cie10', 'estado')
        labels = {
            'tipo_paciente': "Tipo de paciente",
            'tipo_identificacion': "Tipo de identificación",
            'identificacion': "Número de identificación",
            'ciudad_residencia': "Ciudad de residencia",
            'direccion': "Dirección",
            'telefono': "Teléfono",
            'genero': "Género",
            'lugar_nacimiento': "Lugar de nacimiento",
            'motivo_consulta': "Motivo de la consulta",
            'tiempo_evolucion': "Tiempo de evolución",
            'ips_atencion': "IPS de atención primaria",
            'eps': "EPS",
            'nombre_responsable': "Nombre del responsable",
            'parentesco_responsable': "Parentesco del responsable",
            'telefono_responsable': "Teléfono del responsable",
            'evaluacion_inicial': "Evaluación inicial",
            'diagnosticos_cie10': "Diagnósticos cie10",
            'nombre': "Nombre(s)",
            'apellido': "Apellidos",
            'ocupacion': "Ocupación",
            'remitente': "Remitido por",
            'diagnosticador': "Especialista que diagnostica",
            'ocupacion': "Ocupación",
            'escolaridad': "Grado de escolaridad",
        }
        widgets = {
            "enfermedad_actual": forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            "motivo_consulta": forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            "diagnosticos_cie10": Select2MultipleWidget
        }

class AgregarEntradaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario')
        super(AgregarEntradaForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['id'] = "editor1"

        if usuario.cargo in ['Administrador', 'Coordinador']:
            self.fields['area'].queryset = Area.objects.exclude(nombre='Administrativa')
        elif usuario.cargo == 'Terapeuta':
            self.fields['area'].queryset = usuario.area.all()
    
    class Meta:
        model = Entrada
        fields = ('paciente', 'area', 'descripcion')
        labels = {
            'descripcion': "Descripción",
            'area': "Área"
        }
        widgets = {
            'paciente': Select2Widget(),
            'area': Select2Widget(),
            'descripcion': forms.Textarea(attrs={'rows': 10, 'style': 'resize:none;'}),
        }

class VerEntradaForm(forms.ModelForm):
    paciente = forms.ChoiceField(widget=Select2Widget(), initial='')

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario')
        super(VerEntradaForm, self).__init__(*args, **kwargs)

        if usuario.cargo in ['Administrador', 'Coordinador']:
            self.fields['area'].queryset = Area.objects.exclude(nombre='Administrativa')
        elif usuario.cargo == 'Terapeuta':
            self.fields['area'].queryset = usuario.area.all()

    class Meta:
        model = Entrada
        fields = ('empleado', 'paciente', 'descripcion', 'area')
        labels = {
            'area': "Área"
        }
        widgets = {
            'area': Select2Widget()
        }

class ModificarEntradaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        entrada = kwargs.get('instance')
        super(ModificarEntradaForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['id'] = "editor1"
        cargo_empleado = entrada.empleado.cargo
        if cargo_empleado == 'Administrador' or cargo_empleado == 'Coordinador':
            self.fields['area'].queryset = Area.objects.exclude(nombre='Administrativa')
        else:
            self.fields['area'].queryset = entrada.empleado.area.all()

    class Meta:
        model = Entrada
        fields = ('descripcion', 'area')
        labels = {
            'descripcion': "Descripción",
            'area': "Área"
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 10, 'style': 'resize:none;'}),
            'area': Select2Widget()
        }

class CargarCie10Form(forms.Form):
    carga_cie10 = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=["csv"])])
