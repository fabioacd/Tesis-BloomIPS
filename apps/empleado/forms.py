from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectDateWidget
from datetime import datetime
from django_select2.forms import Select2Widget
from bloom_tesis import settings
from .models import Area, Empleado, Resumen
from apps.paciente.models import Eps



# ---------------------AREA----------------------------------------------------------

class AgregarAreaForm(forms.ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea, label="Descripción")

    def __init__(self, *args, **kwargs):
        super(AgregarAreaForm, self).__init__(*args, **kwargs)
        # PlaceHolders
        self.fields['nombre'].widget.attrs['placeholder'] = "Ej. Fisioterapia"
        self.fields['descripcion'].widget.attrs[
            'placeholder'] = "Ej. La fisioterapia, también conocida como terapia física,​ es una disciplina de la salud que ofrece una " \
                             "alternativa terapéutica no farmacológica para diagnosticar, prevenir y tratar síntomas de múltiples dolencias, " \
                             "tanto agudas como crónicas, por medio del ejercicio terapéutico, calor, frío, luz, agua, técnicas manuales " \
                             "entre ellas la electricidad."

    class Meta:
        model = Area
        fields = ('nombre', 'descripcion')

class ModificarAreaForm(forms.ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea, label="Descripción")

    def __init__(self, *args, **kwargs):
        super(ModificarAreaForm, self).__init__(*args, **kwargs)
        # PlaceHolders
        self.fields['nombre'].widget.attrs['placeholder'] = "Ej. Fisioterapia"
        self.fields['descripcion'].widget.attrs[
            'placeholder'] = "Ej. La fisioterapia, también conocida como terapia física,​ es una disciplina de la salud que ofrece una " \
                             "alternativa terapéutica no farmacológica para diagnosticar, prevenir y tratar síntomas de múltiples dolencias, " \
                             "tanto agudas como crónicas, por medio del ejercicio terapéutico, calor, frío, luz, agua, técnicas manuales "
    class Meta:
        model = Area
        fields = ('nombre', 'descripcion')


# ---------------------EPS----------------------------------------------------------
class AgregarEpsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgregarEpsForm, self).__init__(*args, **kwargs)
        self.fields['telefono'].widget.attrs['class'] = "numeric"

        # Placeholders:
        self.fields['nit'].widget.attrs['placeholder'] = "Ej. 41261533-6"
        self.fields['nombre'].widget.attrs['placeholder'] = "Ej. Coomeva EPS"
        self.fields['direccion'].widget.attrs['placeholder'] = "Ej. Carrera 50 #13-21"
        self.fields['telefono'].widget.attrs['placeholder'] = "Ej. 3215458"

    class Meta:
        model = Eps
        fields = ('nit', 'nombre', 'direccion', 'telefono')
        labels = {
            'nit': 'NIT',
            'direccion': 'Dirección',
            'telefono': 'Teléfono'
        }


class ModificarEpsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModificarEpsForm, self).__init__(*args, **kwargs)
        self.fields['telefono'].widget.attrs['class'] = "numeric"

        # Placeholders:
        self.fields['nit'].widget.attrs['placeholder'] = "Ej. 41261533-6"
        self.fields['nombre'].widget.attrs['placeholder'] = "Ej. Coomeva EPS"
        self.fields['direccion'].widget.attrs['placeholder'] = "Ej. Carrera 50 #13-21"
        self.fields['telefono'].widget.attrs['placeholder'] = "Ej. 3215458"

    class Meta:
        model = Eps
        fields = ('nit', 'nombre', 'direccion', 'telefono')
        labels = {
            'nit': 'NIT',
            'direccion': 'Dirección',
            'telefono': 'Teléfono'
        }

#-------------------------EMPLEADO-----------------------------------------------------------------

class AgregarEmpleadoForm(UserCreationForm):
    username = forms.CharField(required=True, label="Número de Identificación")
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", widget=forms.SelectDateWidget())


    def __init__(self, *args, **kwargs):
        super(AgregarEmpleadoForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].required = False
        self.fields['imagen'].help_text = "Si desea modificar su imagen de perfil seleccione una nueva"
        self.fields['username'].widget.attrs['class'] = "numeric"
        self.fields['telefono'].widget.attrs['class'] = "numeric"
        self.fields['celular'].widget.attrs['class'] = "numeric"
        self.fields['first_name'].widget.attrs['class'] = "alphabetic"
        self.fields['last_name'].widget.attrs['class'] = "alphabetic"
        self.fields['fecha_nacimiento'].widget = SelectDateWidget(years=range(1940, datetime.now().year + 1))

        # PlaceHolders
        self.fields['first_name'].widget.attrs['placeholder'] = "Ej. Luis Felipe"
        self.fields['last_name'].widget.attrs['placeholder'] = "Ej. Gómez Castrillon"
        self.fields['direccion'].widget.attrs['placeholder'] = "Ej. Calle 40 #56-34"
        self.fields['telefono'].widget.attrs['placeholder'] = "Ej. 3758990"
        self.fields['celular'].widget.attrs['placeholder'] = "Ej. 3154896325"
        self.fields['email'].widget.attrs['placeholder'] = "Ej. luis.univalle@gmail.com"
        self.fields['username'].widget.attrs['placeholder'] = "Ej. 1144958632"
        self.fields['password1'].widget.attrs['placeholder'] = ""
        self.fields['password2'].widget.attrs['placeholder'] = ""

        imagen = self.instance.imagen
        if imagen:
            self.fields['imagen'].widget.attrs['data-default-file'] = "%s%s" % (settings.MEDIA_URL, imagen.name)

    class Meta:
        model = Empleado
        fields = ('username', 'first_name', 'last_name', 'email', 'telefono', 'celular', 'direccion', 'cargo',
                  'imagen', 'fecha_nacimiento', 'area', 'password1', 'password2')
        widgets = {
            "cargo": Select2Widget(),
            "area": Select2Widget(),
            "imagen": forms.widgets.FileInput(attrs={'class': 'dropify', 'data-height': 150})
        }
        labels = {
            'first_name': 'Nombre(s)',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
        }


class ModificarEmpleadoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModificarEmpleadoForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = "readonly"
        self.fields['imagen'].required = False
        self.fields['username'].widget.attrs['class'] = "numeric"
        self.fields['telefono'].widget.attrs['class'] = "numeric"
        self.fields['celular'].widget.attrs['class'] = "numeric"
        self.fields['first_name'].widget.attrs['class'] = "alphabetic"
        self.fields['last_name'].widget.attrs['class'] = "alphabetic"
        self.fields['imagen'].help_text = "Si desea modificar su imagen de perfil seleccione una nueva"
        self.fields[
            'is_active'].help_text = "Indica si el empleado se encuentra activo actualmente. Desmarque en caso de que el empleado cambie su estado a inactivo."

        # PlaceHolders
        self.fields['first_name'].widget.attrs['placeholder'] = "Ej. Luis Felipe"
        self.fields['last_name'].widget.attrs['placeholder'] = "Ej. Gómez Castrillon"
        self.fields['direccion'].widget.attrs['placeholder'] = "Ej. Calle 40 #56-34"
        self.fields['telefono'].widget.attrs['placeholder'] = "Ej. 3758990"
        self.fields['celular'].widget.attrs['placeholder'] = "Ej. 3154896325"
        self.fields['email'].widget.attrs['placeholder'] = "Ej. luis.univalle@gmail.com"

        imagen = self.instance.imagen
        if imagen:
            self.fields['imagen'].widget.attrs['data-default-file'] = "%s%s" % (settings.MEDIA_URL, imagen.name)

    class Meta:
        model = Empleado
        fields = (
            'username', 'first_name', 'last_name', 'email', 'telefono', 'celular', 'direccion', 'cargo',
            'fecha_nacimiento',
            'area', 'is_active', 'imagen')
        widgets = {
            "imagen": forms.widgets.FileInput(attrs={'class': 'dropify', 'data-height': 150})
        }
        labels = {
            "is_active": "Empleado activo",
            'username': 'Número de identificación',
            'imagen': '',
            'first_name': 'Nombre(s)',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
        }

#------------------------------------------------------RESUMEN-------------------------------------
class AgregarResumenForm(forms.ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(AgregarResumenForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].label = "Descripción del resumen"
        #Placeholders
        self.fields['descripcion'].widget.attrs['placeholder'] = ""
        self.fields['descripcion'].widget.attrs['style'] = "resize:none"


    class Meta:
        model = Resumen
        fields = ('descripcion','paciente')
        widgets = {
            "paciente": Select2Widget(),
        }



class ModificarResumenForm(forms.ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ModificarResumenForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].widget.attrs['readonly'] = "readonly"
        self.fields['descripcion'].label = "Descripción del resumen"
        # Placeholders
        self.fields['descripcion'].widget.attrs['placeholder'] = ""

    class Meta:
        model = Resumen
        fields = ('descripcion', 'paciente', 'revisado')

