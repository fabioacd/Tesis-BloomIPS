from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectDateWidget
import magic
from datetime import datetime
from utils.utils import rango_fechas_informe_mensual
from django_select2.forms import Select2Widget, Select2MultipleWidget
from apps.paciente.models import Eps, Paciente
from bloomips import settings
from .models import Empleado, Area, Resumen, Consolidado
from django import forms


class AgregarEmpleadoForm(UserCreationForm):
    username = forms.CharField(required=True, label="Número de Identificación")
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", widget=forms.SelectDateWidget())

    def __init__(self, *args, **kwargs):
        super(AgregarEmpleadoForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].required = False
        self.fields['firma'].required = False
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
        firma = self.instance.firma
        if imagen:
            self.fields['imagen'].widget.attrs['data-default-file'] = "%s%s" % (settings.MEDIA_URL, imagen.name)
        if firma:
            self.fields['firma'].widget.attrs['data-default-file'] = "%s%s" % (settings.MEDIA_URL, firma.name)

    def clean(self):
        form_data = super().clean()

        if form_data.get('imagen'):
            im_empleado = form_data.get('imagen').read(1048576)
            if magic.from_buffer(im_empleado, mime=True) != 'image/png':
                if magic.from_buffer(im_empleado, mime=True) != 'image/jpeg':
                    self.add_error("imagen", "Únicamente se admiten archivos de tipo 'jpg', 'png' o 'jpeg'")
            else:
                pass

        if form_data.get('firma'):
            firm_empleado = form_data.get('firma').read(1048576)
            if magic.from_buffer(firm_empleado, mime=True) != 'image/png':
                if magic.from_buffer(firm_empleado, mime=True) != 'image/jpeg':
                    self.add_error("firma", "Únicamente se admiten archivos de tipo 'jpg', 'png' o 'jpeg'")
            else:
                pass

        return form_data

    class Meta:
        model = Empleado
        fields = ('username', 'first_name', 'last_name', 'email', 'telefono', 'celular', 'direccion', 'cargo',
                  'imagen', 'fecha_nacimiento', 'area', 'password1', 'password2', 'firma')
        widgets = {
            "cargo": Select2Widget(),
            "area": Select2MultipleWidget(),
            "imagen": forms.widgets.FileInput(attrs={'class': 'dropify', 'data-height': 150}),
            "firma": forms.widgets.FileInput(attrs={'class': 'dropify', 'data-height': 150})
        }
        labels = {
            'first_name': 'Nombre(s)',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
        }


class ModificarEmpleadoForm(forms.ModelForm):
    password1 = forms.CharField(required=False, widget=forms.PasswordInput(), label='Contraseña')
    password2 = forms.CharField(required=False, widget=forms.PasswordInput(), label='Contraseña(confirmación)')

    def __init__(self, *args, **kwargs):
        super(ModificarEmpleadoForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = "readonly"
        self.fields['imagen'].required = False
        self.fields['firma'].required = False
        self.fields['username'].widget.attrs['class'] = "numeric"
        self.fields['telefono'].widget.attrs['class'] = "numeric"
        self.fields['celular'].widget.attrs['class'] = "numeric"
        self.fields['first_name'].widget.attrs['class'] = "alphabetic"
        self.fields['last_name'].widget.attrs['class'] = "alphabetic"
        self.fields['imagen'].help_text = "Si desea modificar su imagen de perfil seleccione una nueva"
        self.fields[
            'is_active'].help_text = "Indica si el empleado se encuentra activo actualmente. " \
                                     "Desmarque en caso de que el empleado cambie su estado a inactivo."

        # PlaceHolders
        self.fields['first_name'].widget.attrs['placeholder'] = "Ej. Luis Felipe"
        self.fields['last_name'].widget.attrs['placeholder'] = "Ej. Gómez Castrillon"
        self.fields['direccion'].widget.attrs['placeholder'] = "Ej. Calle 40 #56-34"
        self.fields['telefono'].widget.attrs['placeholder'] = "Ej. 3758990"
        self.fields['celular'].widget.attrs['placeholder'] = "Ej. 3154896325"
        self.fields['email'].widget.attrs['placeholder'] = "Ej. luis.univalle@gmail.com"

        imagen = self.instance.imagen
        firma = self.instance.firma
        if imagen:
            self.fields['imagen'].widget.attrs['data-default-file'] = "%s%s" % (settings.MEDIA_URL, imagen.name)
        if firma:
            self.fields['firma'].widget.attrs['data-default-file'] = "%s%s" % (settings.MEDIA_URL, firma.name)

    def clean(self):
        form_data = super().clean()
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']

        if pass1 != '' or pass2 != '':
            if pass1 != pass2:
                self.add_error('password2', 'Las contraseñas deben coincidir')
        else:
            pass

        if form_data.get('imagen'):
            im_empleado = form_data.get('imagen').read(1048576)
            if magic.from_buffer(im_empleado, mime=True) != 'image/png':
                if magic.from_buffer(im_empleado, mime=True) != 'image/jpeg':
                    self.add_error("imagen", "Únicamente se admiten archivos de tipo 'jpg', 'png' o 'jpeg'")
            else:
                pass

        if form_data.get('firma'):
            firm_empleado = form_data.get('firma').read(1048576)
            if magic.from_buffer(firm_empleado, mime=True) != 'image/png':
                if magic.from_buffer(firm_empleado, mime=True) != 'image/jpeg':
                    self.add_error("firma", "Únicamente se admiten archivos de tipo 'jpg', 'png' o 'jpeg'")
            else:
                pass

        return form_data

    def save(self, commit=True):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        form = super(ModificarEmpleadoForm, self).save(commit=False)
        if pass1 != '' and pass2 != '':
            form.set_password(pass1)
        if commit:
            form.save()
        return form

    class Meta:
        model = Empleado
        fields = (
            'username', 'first_name', 'last_name', 'email', 'telefono', 'celular', 'direccion', 'cargo',
            'fecha_nacimiento',
            'area', 'is_active', 'imagen', 'firma')
        widgets = {
            "cargo": Select2Widget(),
            "area": Select2MultipleWidget(),
            "imagen": forms.widgets.FileInput(attrs={'class': 'dropify', 'data-height': 150}),
            "firma": forms.widgets.FileInput(attrs={'class': 'dropify', 'data-height': 150})
        }
        labels = {
            "is_active": "Empleado activo",
            'username': 'Número de identificación',
            'first_name': 'Nombre(s)',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
        }


class InformacionPersonalForm(forms.ModelForm):
    pass_actual = forms.CharField(required=False, widget=forms.PasswordInput(), label='Contraseña actual')
    password1 = forms.CharField(required=False, widget=forms.PasswordInput(), label='Nueva contraseña')
    password2 = forms.CharField(required=False, widget=forms.PasswordInput(), label='Nueva contraseña(confirmación)')

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super(InformacionPersonalForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].required = False
        self.fields['telefono'].widget.attrs['class'] = "numeric"
        self.fields['celular'].widget.attrs['class'] = "numeric"
        self.fields['first_name'].widget.attrs['class'] = "alphabetic"
        self.fields['last_name'].widget.attrs['class'] = "alphabetic"
        self.fields['imagen'].help_text = ""

        imagen = self.instance.imagen
        if imagen:
            self.fields['imagen'].widget.attrs['data-default-file'] = "%s%s" % (settings.MEDIA_URL, imagen.name)

    def clean(self):
        form_data = super().clean()
        pass_act = self.cleaned_data['pass_actual']
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']

        if form_data.get('imagen'):
            im_empleado = form_data.get('imagen').read(1048576)
            if magic.from_buffer(im_empleado, mime=True) != 'image/png':
                if magic.from_buffer(im_empleado, mime=True) != 'image/jpeg':
                    self.add_error("imagen", "Únicamente se admiten archivos de tipo 'jpg', 'png' o 'jpeg'")
            else:
                pass

        if pass_act != '':
            if self.usuario.check_password(pass_act):
                if pass1 != '' and pass1 != '':
                    if pass1 == pass2:
                        pass
                    else:
                        self.add_error('password2', 'Las contraseñas deben coincidir')
                else:
                    self.add_error('password1', 'Campos requeridos')
                    self.add_error('password2', 'Campos requeridos')
            else:
                self.add_error('pass_actual', 'Contraseña actual incorrecta')
        elif pass1 != '' or pass1 != '':
            self.add_error('pass_actual', 'Campo requerido')

        return form_data

    def save(self, commit=True):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 != '' and pass2 != '':
            password = self.cleaned_data["password2"]
            self.usuario.set_password(password)
        if commit:
            self.usuario.save()
        return self.usuario

    class Meta:
        model = Empleado
        fields = (
            'first_name', 'last_name', 'email', 'telefono', 'celular', 'direccion', 'fecha_nacimiento', 'imagen')
        widgets = {
            "imagen": forms.widgets.FileInput(attrs={'class': 'dropify', 'data-height': 150})
        }
        labels = {
            'imagen': '',
            'first_name': 'Nombre(s)',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
        }
# ---------------------AREA----------------------------------------------------------


class AgregarAreaForm(forms.ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea, label="Descripción")

    def __init__(self, *args, **kwargs):
        super(AgregarAreaForm, self).__init__(*args, **kwargs)
        # PlaceHolders
        self.fields['nombre'].widget.attrs['placeholder'] = "Ej. Fisioterapia"
        self.fields['descripcion'].widget.attrs[
            'placeholder'] = "Ej. La fisioterapia, también conocida como terapia física,​ es una disciplina " \
                             "de la salud que ofrece una alternativa terapéutica no farmacológica para diagnosticar, " \
                             "prevenir y tratar síntomas de múltiples dolencias, tanto agudas como crónicas, por " \
                             "medio del ejercicio terapéutico, calor, frío, luz, agua, técnicas manuales " \
                             "entre ellas la electricidad."

    class Meta:
        model = Area
        fields = ('nombre', 'descripcion', 'tipo')
        widgets = {
            "tipo": Select2Widget(),
        }


class ModificarAreaForm(forms.ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea, label="Descripción")

    def __init__(self, *args, **kwargs):
        super(ModificarAreaForm, self).__init__(*args, **kwargs)
        # PlaceHolders
        self.fields['nombre'].widget.attrs['placeholder'] = "Ej. Fisioterapia"
        self.fields['descripcion'].widget.attrs[
            'placeholder'] = "Ej. La fisioterapia, también conocida como terapia física,​ es una disciplina " \
                             "de la salud que ofrece una alternativa terapéutica no farmacológica para diagnosticar, " \
                             "prevenir y tratar síntomas de múltiples dolencias, tanto agudas como crónicas, por " \
                             "medio del ejercicio terapéutico, calor, frío, luz, agua, técnicas manuales " \
                             "entre ellas la electricidad."

    class Meta:
        model = Area
        fields = ('nombre', 'descripcion', 'tipo')
        widgets = {
            "tipo": Select2Widget(),
        }


# ------------------------------------------------------RESUMEN-------------------------------------

class VerPacientesInformeMensualForm(forms.Form):
    areas = forms.ModelChoiceField(queryset=Area.objects.exclude(nombre='Administrativa'), widget=Select2Widget())


class AgregarResumenForm(forms.ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario')
        super(AgregarResumenForm, self).__init__(*args, **kwargs)
        rango_fechas = rango_fechas_informe_mensual()
        if usuario.cargo in ['Administrador', 'Coordinador']:
            self.fields['area'].queryset = Area.objects.filter(entradas_area__empleado=usuario, entradas_area__fecha__range=rango_fechas).distinct().exclude(nombre='Administrativa')
        else:
            self.fields['area'].queryset = usuario.area.all()
        self.fields['paciente'].queryset = Paciente.objects.filter(estado='Activo', entradas_paciente__empleado=usuario, entradas_paciente__fecha__range=rango_fechas).distinct()
        self.fields['descripcion'].label = "Descripción del informe mensual"
        self.fields['descripcion'].widget.attrs['id'] = "editor1"
        # Placeholders
        self.fields['descripcion'].widget.attrs['placeholder'] = ""
        self.fields['descripcion'].widget.attrs['style'] = "resize:none"

    class Meta:
        model = Resumen
        fields = ('descripcion', 'paciente', 'area')
        widgets = {
            "paciente": Select2Widget(),
            "area": Select2Widget()
        }


class AgregarResumenEspecificoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        empleados = kwargs.pop('empleados')
        super(AgregarResumenEspecificoForm, self).__init__(*args, **kwargs)
        self.fields['empleado'].queryset = empleados
        self.fields['empleado'].label = "Creado por:"
        self.fields['descripcion'].label = "Descripción del informe mensual"
        self.fields['descripcion'].widget.attrs['id'] = "editor1"
        # Placeholders
        self.fields['descripcion'].widget.attrs['placeholder'] = ""
        self.fields['descripcion'].widget.attrs['style'] = "resize:none"
        self.fields['revisado'].widget.attrs['placeholder'] = ""
        self.fields['revisado'].widget.attrs['data-toggle'] = "toggle"
        self.fields['revisado'].widget.attrs['data-size'] = "small"
        self.fields['revisado'].widget.attrs['data-on'] = "revisado"
        self.fields['revisado'].widget.attrs['data-off'] = "sin revisar"
        self.fields['revisado'].label = ""

    class Meta:
        model = Resumen
        fields = ('descripcion', 'revisado', 'empleado')
        widgets = {
            "descripcion": forms.Textarea,
            "empleado": Select2Widget()
        }


class ModificarResumenForm(forms.ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ModificarResumenForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].label = "Descripción del informe mensual"
        self.fields['descripcion'].widget.attrs['id'] = "editor1"
        # Placeholders
        self.fields['revisado'].widget.attrs['placeholder'] = ""
        self.fields['revisado'].widget.attrs['data-toggle'] = "toggle"
        self.fields['revisado'].widget.attrs['data-size'] = "small"
        self.fields['revisado'].widget.attrs['data-on'] = "revisado"
        self.fields['revisado'].widget.attrs['data-off'] = "sin revisar"
        self.fields['revisado'].label = ""

    class Meta:
        model = Resumen
        fields = ('descripcion',  'revisado')


class VerResumenForm(forms.ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(VerResumenForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].label = "Descripción del informe mensual"
        self.fields['descripcion'].widget.attrs['id'] = "editor1"
        self.fields['descripcion'].widget.attrs['disabled'] = "disabled"

    class Meta:
        model = Resumen
        fields = ('descripcion', 'paciente', 'revisado')


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
