from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django_select2.forms import Select2MultipleWidget, Select2Widget
from .models import ImplicadoEvento, EventoAdverso, TipoEventoAdverso, SeguimientoEvento, ProtocoloLondres


##Implicado

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


##Evento Adverso

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
            "tipos_evento": Select2MultipleWidget(),
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


##Protocolo Londres

class RegistrarProtocoloForm(forms.ModelForm):

    clase_evento = forms.CharField(required=False, label="Clasificación del evento")

    def __init__(self, *args, **kwargs):
        evento = kwargs.pop('evento')
        super(RegistrarProtocoloForm, self).__init__(*args, **kwargs)

        self.fields['clase_evento'].initial = evento.clase_evento
        self.fields['clase_evento'].widget.attrs['disabled'] = "disabled"
        #Placeholders
        self.fields['cronologia'].widget.attrs['placeholder'] = ""
        self.fields['acciones_inseguras'].widget.attrs['placeholder'] = ""
        self.fields['factores_ambiental'].widget.attrs['placeholder'] = ""
        self.fields['factores_equipo'].widget.attrs['placeholder'] = ""
        self.fields['factores_individuo'].widget.attrs['placeholder'] = ""
        self.fields['factores_institucional'].widget.attrs['placeholder'] = ""
        self.fields['factores_organizacion'].widget.attrs['placeholder'] = ""
        self.fields['factores_paciente'].widget.attrs['placeholder'] = ""
        self.fields['factores_tecnologia'].widget.attrs['placeholder'] = ""

        self.fields['actividades'].widget.attrs['placeholder'] = ""
        self.fields['seguimiento'].widget.attrs['placeholder'] = ""

    class Meta:
        model = ProtocoloLondres
        fields = ('cronologia', 'acciones_inseguras', 'factores_ambiental', 'factores_equipo', 'responsable', 'fecha_solucion',
                  'factores_individuo', 'factores_institucional', 'factores_organizacion', 'factores_paciente', 'factores_tecnologia', 'actividades', 'seguimiento')
        widgets = {
            'cronologia': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'acciones_inseguras': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_ambiental': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_equipo': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_individuo': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_institucional': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_organizacion': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_paciente': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_tecnologia': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'actividades': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'seguimiento': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            "fecha_solucion": forms.SelectDateWidget,
            "empleado": Select2Widget(),
        }
        labels = {
            'cronologia': "Cronología del incidente (Reconstruya la cronología y explique qué ocurrió?)",
            'acciones_inseguras': "Acciones inseguras (Por qué ocurrió?)",
            'factores_ambiental': "Factores contributivos relacionados con el ambiente",
            'factores_equipo': "Factores contributivos relacionados con el equipo de trabajo",
            'factores_individuo': "Factores contributivos relacionados con el individuo",
            'factores_institucional': "Factores relacionados con el contexto institucional",
            'factores_organizacion': "Factores contributivos relacionados con organización y gerencia",
            'factores_paciente': "Factores contributivos relacionados con el paciente",
            'factores_tecnologia': "Factores contributivos relacionados con la Tarea y Tecnología",
            'actividades': "Actividades",
            'seguimiento': "Seguimiento",

        }

class ModificarProtocoloForm(forms.ModelForm):

    clase_evento = forms.CharField(required=False, label="Clasificación del evento")

    def __init__(self, *args, **kwargs):
        evento = kwargs.pop('evento')
        super(ModificarProtocoloForm, self).__init__(*args, **kwargs)

        self.fields['clase_evento'].initial = evento.clase_evento
        self.fields['clase_evento'].widget.attrs['disabled'] = "disabled"
        #Placeholders
        self.fields['cronologia'].widget.attrs['placeholder'] = ""
        self.fields['acciones_inseguras'].widget.attrs['placeholder'] = ""
        self.fields['factores_ambiental'].widget.attrs['placeholder'] = ""
        self.fields['factores_equipo'].widget.attrs['placeholder'] = ""
        self.fields['factores_individuo'].widget.attrs['placeholder'] = ""
        self.fields['factores_institucional'].widget.attrs['placeholder'] = ""
        self.fields['factores_organizacion'].widget.attrs['placeholder'] = ""
        self.fields['factores_paciente'].widget.attrs['placeholder'] = ""
        self.fields['factores_tecnologia'].widget.attrs['placeholder'] = ""

        self.fields['actividades'].widget.attrs['placeholder'] = ""
        self.fields['seguimiento'].widget.attrs['placeholder'] = ""

    class Meta:
        model = ProtocoloLondres
        fields = ('cronologia', 'acciones_inseguras', 'factores_ambiental', 'factores_equipo', 'responsable', 'fecha_solucion',
                  'factores_individuo', 'factores_institucional', 'factores_organizacion', 'factores_paciente', 'factores_tecnologia', 'actividades', 'seguimiento')
        widgets = {
            'cronologia': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'acciones_inseguras': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_ambiental': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_equipo': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_individuo': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_institucional': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_organizacion': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_paciente': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_tecnologia': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'actividades': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'seguimiento': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            "fecha_solucion": forms.SelectDateWidget,
            "empleado": Select2Widget(),
        }
        labels = {
            'cronologia': "Cronología del incidente (Reconstruya la cronología y explique qué ocurrió?)",
            'acciones_inseguras': "Acciones inseguras (Por qué ocurrió?)",
            'factores_ambiental': "Factores contributivos relacionados con el ambiente",
            'factores_equipo': "Factores contributivos relacionados con el equipo de trabajo",
            'factores_individuo': "Factores contributivos relacionados con el individuo",
            'factores_institucional': "Factores relacionados con el contexto institucional",
            'factores_organizacion': "Factores contributivos relacionados con organización y gerencia",
            'factores_paciente': "Factores contributivos relacionados con el paciente",
            'factores_tecnologia': "Factores contributivos relacionados con la Tarea y Tecnología",
            'actividades': "Actividades",
            'seguimiento': "Seguimiento",

        }

class VisualizarProtocoloForm(forms.ModelForm):
    clase_evento = forms.CharField(required=False, label="Clasificación del evento")

    def __init__(self, *args, **kwargs):
        evento = kwargs.pop('evento')
        super(VisualizarProtocoloForm, self).__init__(*args, **kwargs)
        self.fields['clase_evento'].initial = evento.clase_evento
        self.fields['clase_evento'].widget.attrs['disabled'] = "disabled"
        # Placeholders
        self.fields['cronologia'].widget.attrs['placeholder'] = ""
        self.fields['acciones_inseguras'].widget.attrs['placeholder'] = ""
        self.fields['factores_ambiental'].widget.attrs['placeholder'] = ""
        self.fields['factores_equipo'].widget.attrs['placeholder'] = ""
        self.fields['factores_individuo'].widget.attrs['placeholder'] = ""
        self.fields['factores_institucional'].widget.attrs['placeholder'] = ""
        self.fields['factores_organizacion'].widget.attrs['placeholder'] = ""
        self.fields['factores_paciente'].widget.attrs['placeholder'] = ""
        self.fields['factores_tecnologia'].widget.attrs['placeholder'] = ""

        self.fields['cronologia'].widget.attrs['readonly'] = True
        self.fields['acciones_inseguras'].widget.attrs['readonly'] = True
        self.fields['factores_ambiental'].widget.attrs['readonly'] = True
        self.fields['factores_equipo'].widget.attrs['readonly'] = True
        self.fields['factores_individuo'].widget.attrs['readonly'] = True
        self.fields['factores_institucional'].widget.attrs['readonly'] = True
        self.fields['factores_organizacion'].widget.attrs['readonly'] = True
        self.fields['factores_paciente'].widget.attrs['readonly'] = True
        self.fields['factores_tecnologia'].widget.attrs['readonly'] = True

        self.fields['fecha_solucion'].widget.attrs['disabled'] = "disabled"
        self.fields['responsable'].widget.attrs['disabled'] = "disabled"

        self.fields['actividades'].widget.attrs['disabled'] = "disabled"
        self.fields['seguimiento'].widget.attrs['disabled'] = "disabled"

    class Meta:
        model = ProtocoloLondres
        fields = ('cronologia', 'acciones_inseguras', 'factores_ambiental', 'factores_equipo', 'responsable', 'fecha_solucion',
                  'factores_individuo', 'factores_institucional', 'factores_organizacion', 'factores_paciente', 'factores_tecnologia', 'actividades', 'seguimiento')
        widgets = {
            'cronologia': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'acciones_inseguras': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_ambiental': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_equipo': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_individuo': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_institucional': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_organizacion': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_paciente': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'factores_tecnologia': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'actividades': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            'seguimiento': forms.Textarea(attrs={'rows': 5, 'style': 'resize:none;'}),
            # "fecha_solucion": forms.SelectDateWidget,
            "empleado": Select2Widget(),
        }
        labels = {
            'cronologia': "Cronología",
            'acciones_inseguras': "Acciones inseguras",
            'factores_ambiental': "Factores contributivos relacionados con el ambiente",
            'factores_equipo': "Factores contributivos relacionados con el equipo de trabajo",
            'factores_individuo': "Factores contributivos relacionados con el individuo",
            'factores_institucional': "Factores relacionados con el contexto institucional",
            'factores_organizacion': "Factores contributivos relacionados con organización y gerencia",
            'factores_paciente': "Factores contributivos relacionados con el paciente",
            'factores_tecnologia': "Factores contributivos relacionados con la Tarea y Tecnología",
            'actividades': "Actividades",
            'seguimiento': "Seguimiento",
            'responsable' : "Responsable de realizar el protocolo",
            'fecha_solucion': "Fecha creación del protocolo"
        }


## Seguimiento Evento Adverso

class AgregarSeguimientoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AgregarSeguimientoForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['placeholder'] = ""

    class Meta:
        model = SeguimientoEvento
        fields = ('fecha', 'descripcion')
        widgets = {
            "descripcion": forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
        }
        labels = {
            'descripcion' : "Descripción"
        }
