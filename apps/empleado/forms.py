from django import forms
from .models import Area



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