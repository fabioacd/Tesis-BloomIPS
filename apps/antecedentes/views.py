from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.serializers import serialize
from django.db import transaction, IntegrityError
from django.forms import formset_factory, modelformset_factory
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
import json

from utils.utils import check_cargos
from .forms import ModificarAntecedentesPersonalesForm, RegistrarAntecedentesPsicosocialesForm, \
    ModificarAntecedentesGestacionalesForm, ModificarAntecedentesFamiliaresForm, \
    VerAntecedentesPersonalesForm, VerAntecedentesGestacionalesForm, VerAntecedenteFamiliaresForm, \
    VerAntecedentesPsicosocialesForm, ModificarAntecedentesPsicosocialesForm, \
    RegistrarAntecedentesPersonalesForm, RegistrarAntecedentesFamiliaresForm, \
    RegistrarAntecedentesGestacionalesForm, RegistrarFamiliarForm
from django.contrib import messages
from .models import AntecedentesPersonales, AntecedentesFamiliares, AntecedentesGestacionales, \
    AntecedentesPsicosociales, Familiar
from apps.paciente.models import Paciente


# Create your views here.


@login_required
def registrar_antecedentes_personales(request):
    form = RegistrarAntecedentesPersonalesForm()

    if request.method == 'POST':
        form = RegistrarAntecedentesPersonalesForm(request.POST)
        if form.is_valid():
            form.save()
            form = RegistrarAntecedentesPersonalesForm()
            messages.success(request, 'Antecedentes registrados')
            if request.POST.get("save_and_records"):
                return redirect(registrar_antecedentes_psicosociales)
        else:
            messages.error(request, 'No se han podido registrar los antecedentes')

    contexto = {'form': form}
    return render(request, 'antecedentes/agregar_antecedentes_personales.html', contexto)


@login_required
def registrar_antecedentes_psicosociales(request):
    form = RegistrarAntecedentesPsicosocialesForm(prefix='antecedentePsicosocial')
    formset = modelformset_factory(Familiar, form=RegistrarFamiliarForm, extra=1)
    formset_familiar = formset(prefix='familiar', queryset=Familiar.objects.none())
    if request.method == 'POST':
        form = RegistrarAntecedentesPsicosocialesForm(request.POST, prefix='antecedentePsicosocial')
        formset_familiar = formset(request.POST, prefix='familiar')
        if form.is_valid():
            if formset_familiar.is_valid():
                try:
                    with transaction.atomic():
                        antecedente = form.save(commit=False)
                        antecedente.save()
                        instancias = formset_familiar.save(commit=False)
                        for familiar in instancias:
                            familiar.antecedente = antecedente
                            familiar.save()
                        messages.success(request, 'Antecedentes registrados')
                except IntegrityError as e:
                    messages.error(request,
                                   'No se han podido registrar los antecedentes debido a un error en la base de datos')

                if request.POST.get("save_and_records"):
                    return redirect(registrar_antecedentes_familiares)
                else:
                    return redirect('registrar_antecedentes_psicosociales')
            else:
                messages.error(request, 'No se han podido guardar los familiares')
        else:
            messages.error(request, 'No se han podido registrar los antecedentes')

    contexto = {'form': form, 'formset_familiar': formset_familiar}
    return render(request, 'antecedentes/agregar_antecedentes_psicosociales.html', contexto)


@login_required
def registrar_antecedentes_gestacionales(request):
    form = RegistrarAntecedentesGestacionalesForm()

    if request.method == 'POST':
        form = RegistrarAntecedentesGestacionalesForm(request.POST)
        if form.is_valid():
            form.save()
            form = RegistrarAntecedentesGestacionalesForm()
            messages.success(request, 'Antecedentes registrados')
            if request.POST.get("save_and_records"):
                return redirect(registrar_antecedentes_personales)
        else:
            messages.error(request, 'No se han podido registrar los antecedentes')

    contexto = {'form': form}
    return render(request, 'antecedentes/agregar_antecedentes_gestacionales.html', contexto)


@login_required
def registrar_antecedentes_familiares(request):
    form = RegistrarAntecedentesFamiliaresForm()

    if request.method == 'POST':
        form = RegistrarAntecedentesFamiliaresForm(request.POST)
        if form.is_valid():
            form.save()
            form = RegistrarAntecedentesFamiliaresForm()
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
    formset = modelformset_factory(Familiar, form=RegistrarFamiliarForm, extra=1)
    formset_familiar = formset(prefix='familiar', queryset=Familiar.objects.none())
    contexto = {'form': VerAntecedentesPsicosocialesForm(), 'formset': formset_familiar}
    return render(request, 'antecedentes/consultar_antecedentes_psicosociales.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Auxiliar administrativo']))
def modificar_antecedentes_gestacionales(request):
    form = ModificarAntecedentesGestacionalesForm()

    if request.method == 'POST':
        antecedente = get_object_or_404(AntecedentesGestacionales, pk=request.POST.get('antecedente'))

        form = ModificarAntecedentesGestacionalesForm(request.POST, instance=antecedente)
        if form.is_valid():
            form.save()
            form = ModificarAntecedentesGestacionalesForm()
            messages.success(request, 'Cambios guardados con éxito')
        else:
            messages.error(request, 'No se han podido guardar los cambios')

    contexto = {'form': form}
    return render(request, 'antecedentes/modificar_antecedentes_gestacionales.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Auxiliar administrativo']))
def modificar_antecedentes_familiares(request):
    form = ModificarAntecedentesFamiliaresForm()

    if request.method == 'POST':
        antecedente = get_object_or_404(AntecedentesFamiliares, pk=request.POST.get('antecedente'))

        form = ModificarAntecedentesFamiliaresForm(request.POST, instance=antecedente)
        if form.is_valid():
            form.save()
            form = ModificarAntecedentesFamiliaresForm()
            messages.success(request, 'Cambios guardados con éxito')
        else:
            messages.error(request, 'No se han podido guardar los cambios')

    contexto = {'form': form}
    return render(request, 'antecedentes/modificar_antecedentes_familiares.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Auxiliar administrativo']))
def modificar_antecedentes_personales(request):
    form = ModificarAntecedentesPersonalesForm()

    if request.method == 'POST':
        antecedente = get_object_or_404(AntecedentesPersonales, pk=request.POST.get('antecedente'))

        form = ModificarAntecedentesPersonalesForm(request.POST, instance=antecedente)
        if form.is_valid():
            form.save()
            form = ModificarAntecedentesPersonalesForm()
            messages.success(request, 'Cambios guardados con éxito')
        else:
            messages.error(request, 'No se han podido guardar los cambios')

    contexto = {'form': form}
    return render(request, 'antecedentes/modificar_antecedentes_personales.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Auxiliar administrativo']))
def modificar_antecedentes_psicosociales(request):
    form = ModificarAntecedentesPsicosocialesForm()
    formset = modelformset_factory(Familiar, form=RegistrarFamiliarForm, can_delete=True)
    formset_familiar = formset(prefix='familiar', queryset=Familiar.objects.none())
    error_formset = False
    if request.method == 'POST':
        antecedente = get_object_or_404(AntecedentesPsicosociales, pk=request.POST.get('antecedente'))
        form = ModificarAntecedentesPsicosocialesForm(request.POST, instance=antecedente)
        formset_familiar = formset(request.POST, prefix='familiar', queryset=Familiar.objects.filter(antecedente=antecedente))
        if form.is_valid():
            if formset_familiar.is_valid():
                try:
                    with transaction.atomic():
                        antecedente = form.save()
                        instancias = formset_familiar.save(commit=False)
                        for obj in formset_familiar.deleted_objects:
                            obj.delete()
                        for familiar in instancias:
                            familiar.antecedente = antecedente
                            familiar.save()
                        messages.success(request, 'Antecedentes registrados')
                except IntegrityError as e:
                    messages.error(request,
                                   'No se han podido modificar los antecedentes debido a un error en la base de datos')
                return redirect('modificar_antecedentes_psicosociales')
            else:
                error_formset = True
                messages.error(request, 'No se han podido guardar los familiares')
        else:
            messages.error(request, 'No se han podido modificar los antecedentes')
    contexto = {'form': form, 'formset_familiar': formset_familiar, 'error_formset': error_formset}
    return render(request, 'antecedentes/modificar_antecedentes_psicosociales.html', contexto)


@login_required
def get_antecedente_personal_ajax(request):
    id_paciente = request.GET.get('id_paciente')
    paciente = get_object_or_404(Paciente, id=id_paciente)
    antecedentes_personales = get_object_or_404(AntecedentesPersonales, paciente=paciente)

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
    paciente = get_object_or_404(Paciente, id=id_paciente)
    antecedentes_gestacionales = get_object_or_404(AntecedentesGestacionales, paciente=paciente)

    if antecedentes_gestacionales is not None:

        antecedentes = {
            'id_antecedente': antecedentes_gestacionales.pk,
            'planeado': antecedentes_gestacionales.planeado,
            'deseado': antecedentes_gestacionales.deseado,
            'controlado': antecedentes_gestacionales.controlado,
            'semanas_gestacion': antecedentes_gestacionales.semanas_gestacion,
            'consumo_embarazo': list(antecedentes_gestacionales.consumo_embarazo.all().values('id')),
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
    paciente = get_object_or_404(Paciente, id=id_paciente)
    antecedentes_familiares = get_object_or_404(AntecedentesFamiliares, paciente=paciente)

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
    paciente = get_object_or_404(Paciente, id=id_paciente)
    try:
        antecedentes_psicosociales = AntecedentesPsicosociales.objects.get(paciente=paciente)
        familiares_queryset = Familiar.objects.filter(antecedente=antecedentes_psicosociales)
        familiares = []
        for familiar in familiares_queryset:
            temp = []
            temp.append(familiar.identificacion_familiar)
            temp.append(familiar.nombre)
            temp.append(familiar.ocupacion)
            temp.append(familiar.escolaridad)
            temp.append(familiar.edad)
            temp.append(familiar.relacion)
            temp.append(str(familiar.id))
            familiares.append(temp)
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
            'familiares': familiares
        }
        datos_json = json.dumps(antecedentes)
        return JsonResponse(datos_json, safe=False)
    else:
        return JsonResponse("", safe=False)