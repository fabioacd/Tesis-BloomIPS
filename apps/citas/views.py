from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
import json

from apps.citas.forms import AgregarCitaForm
from apps.citas.models import Cita
from utils.utils import check_cargos
from django.contrib import messages


# Create your views here.
@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador']))
def consultar_cita(request):
    print('here')
    contexto = {}
    return render(request, 'ver_citas.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador']))
def agregar_cita(request):
    form = AgregarCitaForm()
    if request.method == 'POST':
        form = AgregarCitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.asignador = request.user
            cita.save()
            messages.success(request, 'Cita registrada exitosamente')
            return redirect(consultar_cita)
        else:
            messages.error(request, 'No se pudo registrar la cita')
    citas = Cita.objects.all()
    print(citas)
    contexto = {'form': form, 'citas': citas}
    return render(request, 'agregar_cita.html', contexto)


def modificar_cita(request):
    print('here')
    contexto = {}
    return render(request, 'ver_citas.html', contexto)