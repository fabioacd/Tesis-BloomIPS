from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django_select2.forms import Select2MultipleWidget, Select2Widget
from .models import ImplicadoEvento


class AgregarImplicadoEventoForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre completo")
    id_implicado = forms.CharField(required=True, label="Cédula")
    edad = forms.IntegerField(required=True, label="Edad")
    seguridad_social = forms.CharField(required=True, label="Seguridad social")

    def __init__(self, *args, **kwargs):
        super(AgregarImplicadoEventoForm, self).__init__(*args, **kwargs)
        # self.fields['imagen'].required = False
        self.fields['nombre'].widget.attrs['class'] = "alphabetic"
        self.fields['id_implicado'].widget.attrs['class'] = "numeric"
        self.fields['edad'].widget.attrs['class'] = "numeric"
        #Placeholders
        self.fields['nombre'].widget.attrs['placeholder'] = "Ej. Luis Felipe Gómez Castrillon"
        self.fields['id_implicado'].widget.attrs['placeholder'] = "Ej. 1144958632"
        self.fields['seguridad_social'].widget.attrs['placeholder'] = "Ej. Coomeva EPS"
        self.fields['edad'].widget.attrs['placeholder'] = "Ej. 28"

    def clean(self):
        form_data = super().clean()
        edad = self.cleaned_data['edad']
        if( edad < 0):
            raise forms.ValidationError('La edad no puede ser negativa')
        else:
            pass

        return form_data

    class Meta:
        model = ImplicadoEvento
        fields = ('nombre', 'id_implicado', 'edad', 'seguridad_social')


class ModificarImplicadoEventoAdversoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModificarImplicadoEventoAdversoForm, self).__init__(*args, **kwargs)
        # self.fields['imagen'].required = False
        self.fields['nombre'].widget.attrs['class'] = "alphabetic"
        self.fields['id_implicado'].widget.attrs['class'] = "numeric"
        self.fields['edad'].widget.attrs['class'] = "numeric"
        # Placeholders
        self.fields['nombre'].widget.attrs['placeholder'] = "Ej. Luis Felipe Gómez Castrillon"
        self.fields['id_implicado'].widget.attrs['placeholder'] = "Ej. 1144958632"
        self.fields['seguridad_social'].widget.attrs['placeholder'] = "Ej. Coomeva EPS"
        self.fields['edad'].widget.attrs['placeholder'] = "Ej. 28"

    def clean(self):
        form_data = super().clean()
        edad = self.cleaned_data['edad']
        if (edad < 0):
            raise forms.ValidationError('La edad no puede ser negativa')
        else:
            pass

        return form_data

    class Meta:
        model = ImplicadoEvento
        fields = ('nombre', 'id_implicado', 'edad', 'seguridad_social')