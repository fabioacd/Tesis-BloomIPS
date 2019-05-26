from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget
from .models import AntecedentesPersonales, AntecedentesFamiliares, AntecedentesGestacionales, \
    AntecedentesPsicosociales, Familiar
from apps.paciente.models import Paciente


class RegistrarAntecedentesPersonalesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegistrarAntecedentesPersonalesForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.exclude(
            paciente_personal__in=AntecedentesPersonales.objects.values('paciente')).filter(estado='Activo')

    class Meta:
        model = AntecedentesPersonales
        fields = ('paciente', 'farmacologicos', 'alergicos', 'patologicos', 'toxicos', 'quirurgicos',
                  'prescripcion_medica', 'esquema_vacunacion')
        labels = {
            'farmacologicos': "Farmacológicos",
            'alergicos': "Alérgicos",
            'patologicos': "Patológicos",
            'toxicos': "Tóxicos",
            'quirurgicos': "Quirúrgicos",
            'prescripcion_medica': "Prescripción médica actual (nombre del medicamento, dosis "
                                   "y frecuencia de la dosis)",
            'esquema_vacunacion': "Esquema vacunación",
        }
        widgets = {
            'paciente': Select2Widget(),
            'farmacologicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'alergicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'patologicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'toxicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'quirurgicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'prescripcion_medica': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'esquema_vacunacion': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
        }


class ModificarAntecedentesPersonalesForm(forms.ModelForm):
    antecedente = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(ModificarAntecedentesPersonalesForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.filter(estado='Activo',
                                                                   paciente_personal__in=AntecedentesPersonales.objects.
                                                                   values('paciente'))

    class Meta:
        model = AntecedentesPersonales
        fields = ('paciente', 'farmacologicos', 'alergicos', 'patologicos', 'toxicos', 'quirurgicos',
                  'prescripcion_medica', 'esquema_vacunacion')
        labels = {
            'farmacologicos': "Farmacológicos",
            'alergicos': "Alérgicos",
            'patologicos': "Patológicos",
            'toxicos': "Tóxicos",
            'quirurgicos': "Quirúrgicos",
            'prescripcion_medica': "Prescripción médica actual (nombre del medicamento, dosis "
                                   "y frecuencia de la dosis)",
            'esquema_vacunacion': "Esquema vacunación",
        }
        widgets = {
            'paciente': Select2Widget(),
            'farmacologicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'alergicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'patologicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'toxicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'quirurgicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'prescripcion_medica': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'esquema_vacunacion': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
        }


class VerAntecedentesPersonalesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(VerAntecedentesPersonalesForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.filter(estado='Activo',
                                                                   paciente_personal__in=AntecedentesPersonales.objects.
                                                                   values('paciente'))

        self.fields['farmacologicos'].widget.attrs['readonly'] = "readonly"
        self.fields['alergicos'].widget.attrs['readonly'] = "readonly"
        self.fields['patologicos'].widget.attrs['readonly'] = "readonly"
        self.fields['toxicos'].widget.attrs['readonly'] = "readonly"
        self.fields['quirurgicos'].widget.attrs['readonly'] = "readonly"
        self.fields['prescripcion_medica'].widget.attrs['readonly'] = "readonly"
        self.fields['esquema_vacunacion'].widget.attrs['readonly'] = "readonly"
        self.fields['farmacologicos'].widget.attrs['id'] = "farmacologicos"
        self.fields['alergicos'].widget.attrs['id'] = "alergicos"
        self.fields['patologicos'].widget.attrs['id'] = "patologicos"
        self.fields['toxicos'].widget.attrs['id'] = "toxicos"
        self.fields['quirurgicos'].widget.attrs['id'] = "quirurgicos"
        self.fields['prescripcion_medica'].widget.attrs['id'] = "prescripcion_medica"
        self.fields['esquema_vacunacion'].widget.attrs['id'] = "esquema_vacunacion"
        self.fields['paciente'].widget.attrs['id'] = "paciente"

    class Meta:
        model = AntecedentesPersonales
        fields = ('paciente', 'farmacologicos', 'alergicos', 'patologicos', 'toxicos', 'quirurgicos',
                  'prescripcion_medica', 'esquema_vacunacion')
        labels = {
            'farmacologicos': "Farmacológicos",
            'alergicos': "Alérgicos",
            'patologicos': "Patológicos",
            'toxicos': "Tóxicos",
            'quirurgicos': "Quirúrgicos",
            'prescripcion_medica': "Prescripción médica actual (nombre del medicamento, dosis "
                                   "y frecuencia de la dosis)",
            'esquema_vacunacion': "Esquema vacunación",
        }
        widgets = {
            'paciente': Select2Widget(),
            'farmacologicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'alergicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'patologicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'toxicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'quirurgicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'prescripcion_medica': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'esquema_vacunacion': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
        }


class RegistrarAntecedentesPsicosocialesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegistrarAntecedentesPsicosocialesForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.exclude(
            paciente_psicosocial__in=AntecedentesPsicosociales.objects.values('paciente')).filter(estado='Activo')
        self.fields['tipo_vivienda'].widget.attrs['id'] = "tipo_vivienda"
        self.fields['otro_tipo_vivienda'].widget.attrs['id'] = "otro_tipo_vivienda"
        self.fields['otro_tipo_vivienda'].widget.attrs['disabled'] = "disabled"
        self.fields['otro_tipo_vivienda'].required = False
        self.fields['observacion_servicios'].required = False
        self.fields['observaciones_vivienda'].required = False
        self.fields['lugar_entre_hermanos'].widget.attrs['class'] = "numeric"
        self.fields['numero_habitantes'].widget.attrs['class'] = "numeric"
        self.fields['num_integrantes_laboran'].widget.attrs['class'] = "numeric"
        self.fields['num_hermanos'].widget.attrs['class'] = "numeric"

    class Meta:
        model = AntecedentesPsicosociales
        fields = ('paciente', 'numero_habitantes', 'num_integrantes_laboran', 'lugar_entre_hermanos', 'num_hermanos',
                  'gmfcs', 'observaciones_vivienda', 'observacion_servicios', 'total_ingresos', 'tipo_vivienda',
                  'otro_tipo_vivienda', 'sector_vivienda', 'gas', 'internet', 'agua', 'energia')
        labels = {
            'numero_habitantes': "Número de personas que viven con el paciente",
            'num_integrantes_laboran': "Número de integrantes del hogar que laboran",
            'num_hermanos': "Número de hermanos",
            'lugar_entre_hermanos': "Lugar entre hermanos",
            'tipo_vivienda': "Tipo de vivienda",
            'otro_tipo_vivienda': "Otro tipo de vivienda",
            'total_ingresos': "Total de ingresos",
            'sector_vivienda': "Sector de vivienda",
            'gas': "Gas",
            'internet': "Internet",
            'agua': "Agua",
            'energia': "Energía",
            'gmfcs': "Clasificación de nivel según el sistema de clasificación de la función motriz (GMFCS)",
            'observaciones_vivienda': "Observaciones de vivienda",
            'observacion_servicios': "Observaciones de servicios",
        }
        widgets = {
            'paciente': Select2Widget(),
            'gmfcs': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'observaciones_vivienda': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'observacion_servicios': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
        }


class RegistrarFamiliarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrarFamiliarForm, self).__init__(*args, **kwargs)
        self.fields['identificacion_familiar'].widget.attrs['class'] = 'numeric'
        self.fields['nombre'].widget.attrs['class'] = 'alphabetic'
        self.fields['ocupacion'].widget.attrs['class'] = 'alphabetic'
        self.fields['escolaridad'].widget.attrs['class'] = 'alphabetic'
        self.fields['relacion'].widget.attrs['class'] = 'alphabetic'

    class Meta:
        model = Familiar
        fields = {'identificacion_familiar', 'nombre', 'ocupacion', 'escolaridad', 'edad', 'relacion'}
        labels = {
            'identificacion_familiar': "Identificación",
            'ocupacion': "Ocupación",
            'relacion': "Relación"
        }

        class Media:
            js = ('js/jquery.autocomplete.min.js', 'js/autocomplete-init.js',)
            css = {
                'all': ('css/jquery.autocomplete.css',),
            }


class ModificarAntecedentesPsicosocialesForm(forms.ModelForm):
    antecedente = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(ModificarAntecedentesPsicosocialesForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.filter(estado='Activo',
                                                                   paciente_psicosocial__in=AntecedentesPsicosociales.
                                                                   objects.values('paciente'))
        self.fields['tipo_vivienda'].widget.attrs['id'] = "tipo_vivienda"
        self.fields['otro_tipo_vivienda'].widget.attrs['id'] = "otro_tipo_vivienda"
        self.fields['otro_tipo_vivienda'].widget.attrs['disabled'] = "disabled"
        self.fields['otro_tipo_vivienda'].required = False
        self.fields['observacion_servicios'].required = False
        self.fields['observaciones_vivienda'].required = False
        self.fields['lugar_entre_hermanos'].widget.attrs['class'] = "numeric"
        self.fields['numero_habitantes'].widget.attrs['class'] = "numeric"
        self.fields['num_integrantes_laboran'].widget.attrs['class'] = "numeric"
        self.fields['num_hermanos'].widget.attrs['class'] = "numeric"

    class Meta:
        model = AntecedentesPsicosociales
        fields = ('paciente', 'numero_habitantes', 'num_integrantes_laboran', 'lugar_entre_hermanos', 'num_hermanos',
                  'gmfcs', 'observaciones_vivienda', 'observacion_servicios', 'total_ingresos', 'tipo_vivienda',
                  'otro_tipo_vivienda', 'sector_vivienda', 'gas', 'internet', 'agua', 'energia')
        labels = {
            'numero_habitantes': "Número de personas que viven con el paciente",
            'num_integrantes_laboran': "Número de integrantes del hogar que laboran",
            'num_hermanos': "Número de hermanos",
            'lugar_entre_hermanos': "Lugar entre hermanos",
            'tipo_vivienda': "Tipo de vivienda",
            'otro_tipo_vivienda': "Otro tipo de vivienda",
            'total_ingresos': "Total de ingresos",
            'sector_vivienda': "Sector de vivienda",
            'gas': "Gas",
            'internet': "Internet",
            'agua': "Agua",
            'energia': "Energía",
            'gmfcs': "Clasificación de nivel según el sistema de clasificación de la función motriz (GMFCS)",
            'observaciones_vivienda': "Observaciones de vivienda",
            'observacion_servicios': "Observaciones de servicios",
        }
        widgets = {
            'paciente': Select2Widget(),
            'gmfcs': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'observaciones_vivienda': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'observacion_servicios': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
        }


class VerAntecedentesPsicosocialesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(VerAntecedentesPsicosocialesForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.filter(estado='Activo',
                                                                   paciente_psicosocial__in=AntecedentesPsicosociales.
                                                                   objects.values('paciente'))
        self.fields['numero_habitantes'].widget.attrs['readonly'] = "readonly"
        self.fields['num_integrantes_laboran'].widget.attrs['readonly'] = "readonly"
        self.fields['lugar_entre_hermanos'].widget.attrs['readonly'] = "readonly"
        self.fields['num_hermanos'].widget.attrs['readonly'] = "readonly"
        self.fields['gmfcs'].widget.attrs['readonly'] = "readonly"
        self.fields['observaciones_vivienda'].widget.attrs['readonly'] = "readonly"
        self.fields['observacion_servicios'].widget.attrs['readonly'] = "readonly"
        self.fields['total_ingresos'].widget.attrs['disabled'] = "disabled"
        self.fields['tipo_vivienda'].widget.attrs['disabled'] = "disabled"
        self.fields['otro_tipo_vivienda'].widget.attrs['readonly'] = "readonly"
        self.fields['sector_vivienda'].widget.attrs['disabled'] = "disabled"
        self.fields['gas'].widget.attrs['disabled'] = "disabled"
        self.fields['internet'].widget.attrs['disabled'] = "disabled"
        self.fields['agua'].widget.attrs['disabled'] = "disabled"
        self.fields['energia'].widget.attrs['disabled'] = "disabled"

    class Meta:
        model = AntecedentesPsicosociales
        fields = ('paciente', 'numero_habitantes', 'num_integrantes_laboran', 'lugar_entre_hermanos', 'num_hermanos',
                  'gmfcs', 'observaciones_vivienda', 'observacion_servicios', 'total_ingresos', 'tipo_vivienda',
                  'otro_tipo_vivienda', 'sector_vivienda', 'gas', 'internet', 'agua', 'energia')
        labels = {
            'numero_habitantes': "Número de personas que viven con el paciente",
            'num_integrantes_laboran': "Número de integrantes del hogar que laboran",
            'num_hermanos': "Número de hermanos",
            'lugar_entre_hermanos': "Lugar entre hermanos",
            'tipo_vivienda': "Tipo de vivienda",
            'otro_tipo_vivienda': "Otro tipo de vivienda",
            'total_ingresos': "Total de ingresos",
            'sector_vivienda': "Sector de vivienda",
            'gas': "Gas",
            'internet': "Internet",
            'agua': "Agua",
            'energia': "Energía",
            'gmfcs': "Clasificación de nivel según el sistema de clasificación de la función motriz (GMFCS)",
            'observaciones_vivienda': "Observaciones de vivienda",
            'observacion_servicios': "Observaciones de servicios",
        }
        widgets = {
            'paciente': Select2Widget(),
            'gmfcs': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'observaciones_vivienda': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'observacion_servicios': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'})
        }


class RegistrarAntecedentesGestacionalesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegistrarAntecedentesGestacionalesForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.exclude(paciente_gestacional__in=AntecedentesGestacionales.
                                                                    objects.values('paciente')).\
                                                                    filter(tipo_paciente="Infante", estado='Activo')
        self.fields['otro_consumo'].required = False
        self.fields['otro_sintoma'].required = False
        self.fields['otro_consumo'].widget.attrs['readonly'] = "readonly"
        self.fields['semanas_gestacion'].widget.attrs['class'] = "numeric"

    class Meta:
        model = AntecedentesGestacionales
        fields = ('paciente', 'planeado', 'deseado', 'gemelar', 'controlado', 'consumo_embarazo', 'semanas_gestacion',
                  'parto_termino', 'parto_prematuro', 'amenaza_aborto', 'trabajo_parto_prolongado', 'meconio',
                  'diabetes', 'otro_sintoma', 'otro_consumo', 'circular_cordon', 'placenta_previa', 'torchs', 'cesarea',
                  'preeclamsia', 'forceps')
        labels = {
            'otro_sintoma': "Otro síntoma",
            'otro_consumo': "Otro consumo",
            'consumo_embarazo': "Consumo durante el embarazo de",
            'planeado': "Embarazo planeado",
            'deseado': "Embarazo deseado",
            'controlado': "Embarazo controlado",
            'gemelar': "Parto gemelar",
            'semanas_gestacion': "Semanas de gestación",
            'parto_termino': "Parto a término",
            'parto_prematuro': "Parto prematuro",
            'amenaza_aborto': "Amenaza de aborto",
            'trabajo_parto_prolongado': "Trabajo de parto prolongado",
            'circular_cordon': "Circular de cordón",
            'placenta_previa': "Placenta previa",
            'cesarea': "Cesárea",
            'torchs': "TORCHS",
            'forceps': "Fórceps",
            'preeclamsia': "Pre-eclamsia"
        }
        widgets = {
            'paciente': Select2Widget(),
            'consumo_embarazo': Select2MultipleWidget()
        }


class ModificarAntecedentesGestacionalesForm(forms.ModelForm):
    antecedente = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(ModificarAntecedentesGestacionalesForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.filter(paciente_gestacional__in=AntecedentesGestacionales.
                                                                   objects.values('paciente'),
                                                                   estado='Activo', tipo_paciente="Infante")
        self.fields['otro_consumo'].required = False
        self.fields['otro_sintoma'].required = False
        self.fields['otro_consumo'].widget.attrs['readonly'] = "readonly"
        self.fields['semanas_gestacion'].widget.attrs['class'] = "numeric"

    class Meta:
        model = AntecedentesGestacionales
        fields = ('paciente', 'planeado', 'deseado', 'gemelar', 'controlado', 'consumo_embarazo', 'semanas_gestacion',
                  'parto_termino', 'parto_prematuro', 'amenaza_aborto', 'trabajo_parto_prolongado', 'meconio',
                  'diabetes', 'otro_sintoma', 'otro_consumo','circular_cordon', 'placenta_previa', 'torchs', 'cesarea',
                  'preeclamsia', 'forceps')
        labels = {
            'otro_sintoma': "Otro síntoma",
            'otro_consumo': "Otro consumo",
            'consumo_embarazo': "Consumo durante el embarazo de",
            'planeado': "Embarazo planeado",
            'deseado': "Embarazo deseado",
            'controlado': "Embarazo controlado",
            'gemelar': "Parto gemelar",
            'semanas_gestacion': "Semanas de gestación",
            'parto_termino': "Parto a término",
            'parto_prematuro': "Parto prematuro",
            'amenaza_aborto': "Amenaza de aborto",
            'trabajo_parto_prolongado': "Trabajo de parto prolongado",
            'circular_cordon': "Circular de cordón",
            'placenta_previa': "Placenta previa",
            'cesarea': "Cesárea",
            'torchs': "TORCHS",
            'forceps': "Fórceps",
            'preeclamsia': "Pre-eclamsia"
        }
        widgets = {
            'paciente': Select2Widget(),
            'consumo_embarazo': Select2MultipleWidget()
        }


class VerAntecedentesGestacionalesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(VerAntecedentesGestacionalesForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.filter(paciente_gestacional__in=AntecedentesGestacionales.
                                                                   objects.values('paciente'),
                                                                   estado='Activo', tipo_paciente="Infante")

        self.fields['consumo_embarazo'].widget.attrs['disabled'] = "disabled"
        self.fields['planeado'].widget.attrs['disabled'] = "disabled"
        self.fields['deseado'].widget.attrs['disabled'] = "disabled"
        self.fields['controlado'].widget.attrs['disabled'] = "disabled"
        self.fields['gemelar'].widget.attrs['disabled'] = "disabled"
        self.fields['consumo_embarazo'].widget.attrs['disabled'] = "disabled"
        self.fields['semanas_gestacion'].widget.attrs['disabled'] = "disabled"
        self.fields['parto_termino'].widget.attrs['disabled'] = "disabled"
        self.fields['parto_prematuro'].widget.attrs['disabled'] = "disabled"
        self.fields['amenaza_aborto'].widget.attrs['disabled'] = "disabled"
        self.fields['trabajo_parto_prolongado'].widget.attrs['disabled'] = "disabled"
        self.fields['circular_cordon'].widget.attrs['disabled'] = "disabled"
        self.fields['placenta_previa'].widget.attrs['disabled'] = "disabled"
        self.fields['cesarea'].widget.attrs['disabled'] = "disabled"
        self.fields['torchs'].widget.attrs['disabled'] = "disabled"
        self.fields['forceps'].widget.attrs['disabled'] = "disabled"
        self.fields['meconio'].widget.attrs['disabled'] = "disabled"
        self.fields['diabetes'].widget.attrs['disabled'] = "disabled"
        self.fields['preeclamsia'].widget.attrs['disabled'] = "disabled"
        self.fields['otro_consumo'].widget.attrs['readonly'] = "readonly"
        self.fields['otro_sintoma'].widget.attrs['readonly'] = "readonly"

    class Meta:
        model = AntecedentesGestacionales
        fields = ('paciente', 'planeado', 'deseado', 'gemelar', 'controlado', 'consumo_embarazo', 'semanas_gestacion',
                  'parto_termino', 'parto_prematuro', 'amenaza_aborto', 'trabajo_parto_prolongado', 'meconio',
                  'diabetes', 'otro_sintoma', 'otro_consumo','circular_cordon', 'placenta_previa', 'torchs', 'cesarea',
                  'preeclamsia', 'forceps')
        labels = {
            'otro_sintoma': "Otro síntoma",
            'otro_consumo': "Otro consumo",
            'consumo_embarazo': "Consumo durante el embarazo de",
            'planeado': "Embarazo planeado",
            'deseado': "Embarazo deseado",
            'controlado': "Embarazo controlado",
            'gemelar': "Parto gemelar",
            'semanas_gestacion': "Semanas de gestación",
            'parto_termino': "Parto a término",
            'parto_prematuro': "Parto prematuro",
            'amenaza_aborto': "Amenaza de aborto",
            'trabajo_parto_prolongado': "Trabajo de parto prolongado",
            'circular_cordon': "Circular de cordón",
            'placenta_previa': "Placenta previa",
            'cesarea': "Cesárea",
            'torchs': "TORCHS",
            'forceps': "Fórceps",
            'preeclamsia': "Pre-eclamsia"
        }
        widgets = {
            'paciente': Select2Widget(),
            'consumo_embarazo': Select2MultipleWidget()
        }


class RegistrarAntecedentesFamiliaresForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegistrarAntecedentesFamiliaresForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.exclude(
            paciente_familiar__in=AntecedentesFamiliares.objects.values('paciente')).filter(estado='Activo')

    class Meta:
        model = AntecedentesFamiliares
        fields = ('paciente', 'enfermedad_madre', 'enfermedad_padre', 'enfermedad_hermanos', 'otros_antecedentes',
                  'antecedentes_clinicos')
        labels = {
            'enfermedad_madre': "Enfermedades que padece la madre",
            'enfermedad_padre': "Enfermedades que padece el padre",
            'enfermedad_hermanos': "Enfermedades que padecen los hermanos",
            'otros_antecedentes': "Otros antecedentes (Abuelos - tíos)",
            'antecedentes_clinicos': "Antecedentes clínicos"
        }
        widgets = {
            'paciente': Select2Widget(),
            'enfermedad_madre': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'enfermedad_padre': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'enfermedad_hermanos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'otros_antecedentes': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'antecedentes_clinicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
        }


class ModificarAntecedentesFamiliaresForm(forms.ModelForm):
    antecedente = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(ModificarAntecedentesFamiliaresForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.filter(estado='Activo',
                                                                   paciente_familiar__in=AntecedentesFamiliares.
                                                                   objects.values('paciente'))

    class Meta:
        model = AntecedentesFamiliares
        fields = ('paciente', 'enfermedad_madre', 'enfermedad_padre', 'enfermedad_hermanos', 'otros_antecedentes',
                  'antecedentes_clinicos')
        labels = {
            'enfermedad_madre': "Enfermedades que padece la madre",
            'enfermedad_padre': "Enfermedades que padece el padre",
            'enfermedad_hermanos': "Enfermedades que padecen los hermanos",
            'otros_antecedentes': "Otros antecedentes (Abuelos - tíos)",
            'antecedentes_clinicos': "Antecedentes clínicos"
        }
        widgets = {
            'paciente': Select2Widget(),
            'enfermedad_madre': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'enfermedad_padre': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'enfermedad_hermanos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'otros_antecedentes': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'antecedentes_clinicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
        }


class VerAntecedenteFamiliaresForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(VerAntecedenteFamiliaresForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.filter(estado='Activo',
                                                                   paciente_familiar__in=AntecedentesFamiliares.objects.
                                                                   values('paciente'))
        self.fields['enfermedad_madre'].widget.attrs['readonly'] = "readonly"
        self.fields['enfermedad_padre'].widget.attrs['readonly'] = "readonly"
        self.fields['enfermedad_hermanos'].widget.attrs['readonly'] = "readonly"
        self.fields['otros_antecedentes'].widget.attrs['readonly'] = "readonly"
        self.fields['antecedentes_clinicos'].widget.attrs['readonly'] = "readonly"

    class Meta:
        model = AntecedentesFamiliares
        fields = ('paciente', 'enfermedad_madre', 'enfermedad_padre', 'enfermedad_hermanos', 'otros_antecedentes',
                  'antecedentes_clinicos')
        labels = {
            'enfermedad_madre': "Enfermedades que padece la madre",
            'enfermedad_padre': "Enfermedades que padece el padre",
            'enfermedad_hermanos': "Enfermedades que padecen los hermanos",
            'otros_antecedentes': "Otros antecedentes (Abuelos - tíos)",
            'antecedentes_clinicos': "Antecedentes clínicos"
        }
        widgets = {
            'paciente': Select2Widget(),
            'enfermedad_madre': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'enfermedad_padre': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'enfermedad_hermanos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'otros_antecedentes': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
            'antecedentes_clinicos': forms.Textarea(attrs={'rows': 7, 'style': 'resize:none;'}),
        }
