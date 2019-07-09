from imghdr import test_rast

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
import json

from apps.citas.forms import AgregarCitaForm, ModificarCitaForm
from apps.citas.models import Cita
from utils.utils import check_cargos
from django.contrib import messages


# Create your views here.
@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador']))
def modificar_cita(request, id_cita):
    cita = get_object_or_404(Cita, id=id_cita)
    if request.method == 'POST':
        form = ModificarCitaForm(request.POST, instance=cita)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.asignador = request.user
            cita.save()
            messages.success(request, 'Cita registrada exitosamente')
            return redirect(consultar_cita)
        else:
            messages.error(request, 'No se pudo registrar la cita')
    else:
        form = ModificarCitaForm(instance=cita)
    contexto = {'form': form}
    return render(request, 'ver_cita.html', contexto)

@login_required
@user_passes_test(check_cargos(['Administrador']))
def agregar_cita(request):
    form = AgregarCitaForm()
    if request.method == 'POST':
        form = AgregarCitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.asignador = request.user
            hora_ini = cita.hora.replace(hour=(cita.hora.hour - 1) % 24)
            hora_fin = cita.hora.replace(hour=(cita.hora.hour + 1) % 24)
            print("Horas: ", hora_ini, hora_fin, cita.hora)
            citas = Cita.objects.filter(hora__range=[hora_ini, hora_fin], fecha=cita.fecha, terapeuta=cita.terapeuta)
            print(citas)
            if not citas:
                cita.save()
                messages.success(request, 'Cita registrada exitosamente')
            else:
                messages.error(request, 'No se pudo registrar la cita')
            return redirect(agregar_cita)
        else:
            messages.error(request, 'No se pudo registrar la cita')
    citas = Cita.objects.all()
    contexto = {'form': form, 'citas': citas}
    return render(request, 'agregar_cita.html', contexto)


def consultar_cita(request):
    print('here')
    contexto = {}
    return render(request, 'ver_cita.html', contexto)

def get_info_cita(request):
    id_cita = request.GET.get('id_cita')
    cita = Cita.objects.get(id=id_cita)
    json_data = {
        'id_cita': cita.id,
        'paciente_cita': cita.paciente.identificacion + ' - ' + cita.paciente.nombre + ' ' + cita.paciente.apellido,
        'terapeuta_cita': cita.terapeuta.first_name + ' ' + cita.terapeuta.last_name,
        'fecha_cita': cita.fecha,
        'hora_cita': cita.hora
    }
    return JsonResponse(json_data, safe=False)

def cancelar_cita(request):
    id_cita = request.GET.get('id_cita')
    cita = Cita.objects.get(id=id_cita)
    status_delete = cita.delete()
    if status_delete[0] == 1:
        status = True
    else:
        status = False
    json_data = {
        'status': status,
    }
    return JsonResponse(json_data, safe=False)