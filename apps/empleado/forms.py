from django import forms
from .models import Area
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

