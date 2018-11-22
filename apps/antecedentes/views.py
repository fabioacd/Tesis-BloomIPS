from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .forms import RegistrarModificarAntecedentesPersonalesForm, RegistrarModificarAntecedentesPsicosocialesForm, \
                    RegistrarModificarAntecedentesGestacionalesForm, RegistrarModificarAntecedenteFamiliaresForm, \
                    VerAntecedentesPersonalesForm, VerAntecedentesGestacionalesForm, VerAntecedenteFamiliaresForm, \
                    VerAntecedentesPsicosocialesForm
from django.contrib import messages
from .models import AntecedentesPersonales, AntecedentesFamiliares, AntecedentesGestacionales, AntecedentesPsicosociales
from apps.paciente.models import Paciente
# Create your views here.

@login_required
def registrar_antecedentes_personales(request):
    form = RegistrarModificarAntecedentesPersonalesForm()

    if request.method == 'POST':
        form = RegistrarModificarAntecedentesPersonalesForm(request.POST)
        if form.is_valid():
            form.save()
            form = RegistrarModificarAntecedentesPersonalesForm()
            messages.success(request, 'Antecedentes registrados')
        else:
            messages.error(request, 'No se han podido registrar los antecedentes')

    contexto = {'form': form}
    return render(request, 'antecedentes/agregar_antecedentes_personales.html', contexto)

@login_required
def registrar_antecedentes_psicosociales(request):
    form = RegistrarModificarAntecedentesPsicosocialesForm()

    if request.method == 'POST':
        form = RegistrarModificarAntecedentesPsicosocialesForm(request.POST)
        if form.is_valid():
            form.save()
            form = RegistrarModificarAntecedentesPsicosocialesForm()
            messages.success(request, 'Antecedentes registrados')
        else:
            messages.error(request, 'No se han podido registrar los antecedentes')

    contexto = {'form': form}
    return render(request, 'antecedentes/agregar_antecedentes_psicosociales.html', contexto)

@login_required
def registrar_antecedentes_gestacionales(request):
    form = RegistrarModificarAntecedentesGestacionalesForm()

    if request.method == 'POST':
        form = RegistrarModificarAntecedentesGestacionalesForm(request.POST)
        if form.is_valid():
            form.save()
            form = RegistrarModificarAntecedentesGestacionalesForm()
            messages.success(request, 'Antecedentes registrados')
        else:
            messages.error(request, 'No se han podido registrar los antecedentes')

    contexto = {'form': form}
    return render(request, 'antecedentes/agregar_antecedentes_gestacionales.html', contexto)

@login_required
def registrar_antecedentes_familiares(request):
    form = RegistrarModificarAntecedenteFamiliaresForm()

    if request.method == 'POST':
        form = RegistrarModificarAntecedenteFamiliaresForm(request.POST)
        if form.is_valid():
            form.save()
            form = RegistrarModificarAntecedenteFamiliaresForm()
            messages.success(request, 'Antecedentes registrados')
        else:
            messages.error(request, 'No se han podido registrar los antecedentes')

    contexto = {'form': form}
    return render(request, 'antecedentes/agregar_antecedentes_familiares.html', contexto)

@login_required
def consultar_antecedentes_personales(request):
    contexto = {'form': VerAntecedentesPersonalesForm()}
    return render(request, 'antecedentes/consultar_antecedentes_personales.html', contexto)

@login_required
def consultar_antecedentes_gestacionales(request):
    contexto = {'form': VerAntecedentesGestacionalesForm()}
    return render(request, 'antecedentes/consultar_antecedentes_gestacionales.html', contexto)

@login_required
def consultar_antecedentes_familiares(request):
    contexto = {'form': VerAntecedenteFamiliaresForm()}
    return render(request, 'antecedentes/consultar_antecedentes_familiares.html', contexto)

@login_required
def consultar_antecedentes_psicosociales(request):
    contexto = {'form': VerAntecedentesPsicosocialesForm()}
    return render(request, 'antecedentes/consultar_antecedentes_psicosociales.html', contexto)


def modificar_antecedentes_gestacionales(request):
    form = RegistrarModificarAntecedentesGestacionalesForm()

    if request.method == 'POST':
        antecedente = None

        try:
            antecedente = AntecedentesGestacionales.objects.get(pk=request.POST.get('antecedente'))
        except AntecedentesGestacionales.DoesNotExist:
            pass

        form = RegistrarModificarAntecedentesGestacionalesForm(request.POST, instance=antecedente)
        if form.is_valid():
            form.save()
            form = RegistrarModificarAntecedentesGestacionalesForm()
            messages.success(request, 'Cambios guardados con éxito')
        else:
            messages.error(request, 'No se han podido guardar los cambios')

    contexto = {'form': form}
    return render(request, 'antecedentes/modificar_antecedentes_gestacionales.html', contexto)

@login_required
def modificar_antecedentes_familiares(request):

    form = RegistrarModificarAntecedenteFamiliaresForm()

    if request.method == 'POST':
        antecedente = None

        try:
            antecedente = AntecedentesFamiliares.objects.get(pk=request.POST.get('antecedente'))
        except AntecedentesFamiliares.DoesNotExist:
            pass

        form = RegistrarModificarAntecedenteFamiliaresForm(request.POST, instance=antecedente)
        if form.is_valid():
            form.save()
            form = RegistrarModificarAntecedenteFamiliaresForm()
            messages.success(request, 'Cambios guardados con éxito')
        else:
            messages.error(request, 'No se han podido guardar los cambios')

    contexto = {'form': form}
    return render(request, 'antecedentes/modificar_antecedentes_familiares.html', contexto)

@login_required
def modificar_antecedentes_personales(request):
    form = RegistrarModificarAntecedentesPersonalesForm()

    if request.method == 'POST':
        antecedente = None

        try:
            antecedente = AntecedentesPersonales.objects.get(pk=request.POST.get('antecedente'))
        except AntecedentesPersonales.DoesNotExist:
            pass

        form = RegistrarModificarAntecedentesPersonalesForm(request.POST, instance=antecedente)
        if form.is_valid():
            form.save()
            form = RegistrarModificarAntecedentesPersonalesForm()
            messages.success(request, 'Cambios guardados con éxito')
        else:
            messages.error(request, 'No se han podido guardar los cambios')

    contexto = {'form': form}
    return render(request, 'antecedentes/modificar_antecedentes_personales.html', contexto)

@login_required
def modificar_antecedentes_psicosociales(request):
    form = RegistrarModificarAntecedentesPsicosocialesForm()

    if request.method == 'POST':
        antecedente = None

        try:
            antecedente = AntecedentesPsicosociales.objects.get(pk=request.POST.get('antecedente'))
        except AntecedentesPsicosociales.DoesNotExist:
            pass

        form = RegistrarModificarAntecedentesPsicosocialesForm(request.POST, instance=antecedente)
        if form.is_valid():
            form.save()
            form = RegistrarModificarAntecedentesPsicosocialesForm()
            messages.success(request, 'Cambios guardados con éxito')
        else:
            messages.error(request, 'No se han podido guardar los cambios')

    contexto = {'form': form}
    return render(request, 'antecedentes/modificar_antecedentes_psicosociales.html', contexto)

@login_required
def get_antecedente_personal_ajax(request):

    id_paciente = request.GET.get('id_paciente')
    paciente = Paciente.objects.get(identificacion=id_paciente)
    try:
        antecedentes_personales = AntecedentesPersonales.objects.get(paciente=paciente)
    except AntecedentesPersonales.DoesNotExist:
        antecedentes_personales = None

    if antecedentes_personales is not None:

        antecedentes = {
            'id_antecedente': antecedentes_personales.pk,
            'farmacologicos': antecedentes_personales.farmacologicos,
            'alergicos': antecedentes_personales.alergicos,
            'patologicos': antecedentes_personales.patologicos,
            'toxicos': antecedentes_personales.toxicos,
            'quirurgicos': antecedentes_personales.quirurgicos,
            'prescripcion_medica': antecedentes_personales.prescripcion_medica,
            'esquema_vacunacion': antecedentes_personales.esquema_vacunacion
        }
        datos_json = json.dumps(antecedentes)
        return JsonResponse(datos_json, safe=False)
    else:
        return JsonResponse("", safe=False)

@login_required
def get_antecedente_gestacional_ajax(request):

    id_paciente = request.GET.get('id_paciente')
    paciente = Paciente.objects.get(identificacion=id_paciente)
    try:
        antecedentes_gestacionales = AntecedentesGestacionales.objects.get(paciente=paciente)
    except AntecedentesGestacionales.DoesNotExist:
        antecedentes_gestacionales = None

    if antecedentes_gestacionales is not None:

        antecedentes = {
            'id_antecedente': antecedentes_gestacionales.pk,
            'planeado': antecedentes_gestacionales.planeado,
            'deseado': antecedentes_gestacionales.deseado,
            'controlado': antecedentes_gestacionales.controlado,
            'semanas_gestacion': antecedentes_gestacionales.semanas_gestacion,
            'consumo_embarazo': antecedentes_gestacionales.consumo_embarazo.id,
            'otro_consumo': antecedentes_gestacionales.otro_consumo,
            'gemelar': antecedentes_gestacionales.gemelar,
            'parto_termino': antecedentes_gestacionales.parto_termino,
            'parto_prematuro': antecedentes_gestacionales.parto_prematuro,
            'amenaza_aborto': antecedentes_gestacionales.amenaza_aborto,
            'trabajo_parto_prolongado': antecedentes_gestacionales.trabajo_parto_prolongado,
            'meconio': antecedentes_gestacionales.meconio,
            'diabetes': antecedentes_gestacionales.diabetes,
            'placenta_previa': antecedentes_gestacionales.placenta_previa,
            'circular_cordon': antecedentes_gestacionales.circular_cordon,
            'torchs': antecedentes_gestacionales.torchs,
            'cesarea': antecedentes_gestacionales.cesarea,
            'preeclamsia': antecedentes_gestacionales.preeclamsia,
            'forceps': antecedentes_gestacionales.forceps,
            'otro_sintoma': antecedentes_gestacionales.otro_sintoma
        }
        datos_json = json.dumps(antecedentes)
        return JsonResponse(datos_json, safe=False)
    else:
        return JsonResponse("", safe=False)

@login_required
def get_antecedente_familiar_ajax(request):

    id_paciente = request.GET.get('id_paciente')
    paciente = Paciente.objects.get(identificacion=id_paciente)
    try:
        antecedentes_familiares = AntecedentesFamiliares.objects.get(paciente=paciente)
    except AntecedentesFamiliares.DoesNotExist:
        antecedentes_familiares = None

    if antecedentes_familiares is not None:

        antecedentes = {
            'id_antecedente': antecedentes_familiares.pk,
            'enfermedad_madre': antecedentes_familiares.enfermedad_madre,
            'enfermedad_padre': antecedentes_familiares.enfermedad_padre,
            'enfermedad_hermanos': antecedentes_familiares.enfermedad_hermanos,
            'antecedentes_clinicos': antecedentes_familiares.antecedentes_clinicos,
            'otros_antecedentes': antecedentes_familiares.otros_antecedentes
        }
        datos_json = json.dumps(antecedentes)
        return JsonResponse(datos_json, safe=False)
    else:
        return JsonResponse("", safe=False)

@login_required
def get_antecedentes_psicosocial_ajax(request):

    id_paciente = request.GET.get('id_paciente')
    paciente = Paciente.objects.get(identificacion=id_paciente)
    try:
        antecedentes_psicosociales = AntecedentesPsicosociales.objects.get(paciente=paciente)
    except AntecedentesPsicosociales.DoesNotExist:
        antecedentes_psicosociales = None

    if antecedentes_psicosociales is not None:

        antecedentes = {
            'id_antecedente': antecedentes_psicosociales.pk,
            'gas': antecedentes_psicosociales.gas,
            'internet': antecedentes_psicosociales.internet,
            'agua': antecedentes_psicosociales.agua,
            'energia': antecedentes_psicosociales.energia,
            'numero_habitantes': antecedentes_psicosociales.numero_habitantes,
            'num_integrantes_laboran': antecedentes_psicosociales.num_integrantes_laboran,
            'num_hermanos': antecedentes_psicosociales.num_hermanos,
            'lugar_entre_hermanos': antecedentes_psicosociales.lugar_entre_hermanos,
            'total_ingresos': antecedentes_psicosociales.total_ingresos,
            'tipo_vivienda': antecedentes_psicosociales.tipo_vivienda.id,
            'otro_tipo_vivienda': antecedentes_psicosociales.otro_tipo_vivienda,
            'sector_vivienda': antecedentes_psicosociales.sector_vivienda,
            'observaciones_vivienda': antecedentes_psicosociales.observaciones_vivienda,
            'observacion_servicios': antecedentes_psicosociales.observacion_servicios,
            'gmfcs': antecedentes_psicosociales.gmfcs,
        }
        datos_json = json.dumps(antecedentes)
        return JsonResponse(datos_json, safe=False)
    else:
        return JsonResponse("", safe=False)
