from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django_select2.forms import Select2MultipleWidget, Select2Widget
from apps.citas.models import Cita


class AgregarCitaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AgregarCitaForm, self).__init__(*args, **kwargs)
        self.fields['hora'].widget.attrs['placeholder'] = "Ej. 09:45"
        self.fields['fecha'].widget.attrs['placeholder'] = "Ej. 05/06/2007"

    class Meta:
        model = Cita
        fields = ('terapeuta', 'paciente', 'hora', 'fecha')
        widgets = {
            "terapeuta": Select2Widget(),
            "paciente": Select2Widget(),
            "hora": forms.TimeInput(format='%H:%M')
        }