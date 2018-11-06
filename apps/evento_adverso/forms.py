from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django_select2.forms import Select2MultipleWidget, Select2Widget
from .models import ImplicadoEvento, EventoAdverso, TipoEventoAdverso

#---------------------IMPLICADO A EVENTO ADVERSO-----------------------------------------------------

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


#---------------------EVENTO ADVERSO-----------------------------------------------------

class AgregarEventoAdversoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgregarEventoAdversoForm, self).__init__(*args, **kwargs)
        #Placeholders
        self.fields['hora'].widget.attrs['placeholder'] = "Ej. 09:45"
        self.fields['fecha_ocurrencia'].widget.attrs['placeholder'] = "Ej. 05/06/2007"
        self.fields['otro_tipo_evento'].widget.attrs['placeholder'] = "Ej: Fractura"
        self.fields['lugar'].widget.attrs['placeholder'] = "Ej: Sala de espera"
        self.fields['causa'].widget.attrs['placeholder'] = ""
        self.fields['descripcion'].widget.attrs['placeholder'] = ""
        self.fields['acciones_realizadas'].widget.attrs['placeholder'] = ""


    class Meta:
        model = EventoAdverso
        fields = (
        'implicado', 'clase_evento', 'lugar', 'fecha_ocurrencia', 'fecha_reporte', 'hora', 'causa',
        'acciones_realizadas', 'descripcion', 'tipos_evento', 'otro_tipo_evento', 'empleado')
        widgets = {
            "implicado": Select2Widget(),
            "empleado": Select2Widget(),
            "tipos_evento": Select2MultipleWidget(),
            "causa": forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            "descripcion": forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            "acciones_realizadas": forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            "fecha_reporte": forms.SelectDateWidget,
            "hora": forms.TimeInput(format='%H:%M'),
            "fecha_ocurrencia": forms.TextInput,
        }
        labels = {
            'tipos_evento' : 'Tipos de incidentes',
            'otro_tipo_evento' : 'Otro tipo de incidente',
            'hora' : 'Hora de ocurrencia',
            'fecha_ocurrencia' : 'Fecha de ocurrencia',
            'descripcion' : 'Descripción'
        }

    # def clean_causa(self):
    #     causa = self.cleaned_data['causa']
    #
    #     if( "fabio" not in causa):
    #         raise forms.ValidationError('causa debe ser fabio')
    #
    #
    #     return causa
    #
    # def clean_hora(self):
    #     hora = self.cleaned_data['hora']
    #
    #     return hora
    #
    def clean(self):
        form_data = super().clean()
        tipos_evento = form_data.get('tipos_evento')
        if tipos_evento:
            try:
                if TipoEventoAdverso.objects.get(nombre='Otro') in tipos_evento:
                    otro_tipo_evento = form_data.get('otro_tipo_evento')

                    if not otro_tipo_evento or otro_tipo_evento == "":
                        self.add_error('otro_tipo_evento', 'Este campo es requerido')
                else:
                    form_data['otro_tipo_evento'] = ""
            except ObjectDoesNotExist:
                form_data['otro_tipo_evento'] = ""

        return form_data

class ModificarEventoAdversoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModificarEventoAdversoForm, self).__init__(*args, **kwargs)
        #Placeholders
        self.fields['hora'].widget.attrs['placeholder'] = "Ej. 09:45"
        self.fields['fecha_ocurrencia'].widget.attrs['placeholder'] = "Ej. 05/06/2007"
        self.fields['otro_tipo_evento'].widget.attrs['placeholder'] = "Ej: Fractura"
        self.fields['lugar'].widget.attrs['placeholder'] = "Ej: Sala de espera"
        self.fields['causa'].widget.attrs['placeholder'] = ""
        self.fields['descripcion'].widget.attrs['placeholder'] = ""
        self.fields['acciones_realizadas'].widget.attrs['placeholder'] = ""


    class Meta:
        model = EventoAdverso
        fields = (
        'implicado', 'clase_evento', 'lugar', 'fecha_ocurrencia', 'fecha_reporte', 'hora', 'causa',
        'acciones_realizadas', 'descripcion', 'tipos_evento', 'otro_tipo_evento')
        widgets = {
            "implicado": Select2Widget(),
            "empleado": Select2Widget(),
            "tipos_evento": Select2MultipleWidget(
                # queryset=TipoEventoAdverso.objects.all(),
                # model=TipoEventoAdverso,
            ),
            "causa": forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            "descripcion": forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            "acciones_realizadas": forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            "fecha_reporte": forms.SelectDateWidget,
            "hora": forms.TimeInput(format='%H:%M'),
        }
        labels = {
            'tipos_evento': 'Tipos de incidentes',
            'otro_tipo_evento': 'Otro tipo de incidente',
            'hora': 'Hora de ocurrencia',
            'fecha_ocurrencia': 'Fecha de ocurrencia',
            'descripcion': 'Descripción'
        }

    def clean(self):
        form_data = super().clean()
        tipos_evento = form_data.get('tipos_evento')
        if tipos_evento:
            try:
                if TipoEventoAdverso.objects.get(nombre='Otro') in tipos_evento:
                    otro_tipo_evento = form_data.get('otro_tipo_evento')

                    if not otro_tipo_evento or otro_tipo_evento == "":
                        self.add_error('otro_tipo_evento', 'Este campo es requerido')
                else:
                    form_data['otro_tipo_evento'] = ""
            except ObjectDoesNotExist:
                form_data['otro_tipo_evento'] = ""

        return form_data