from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .forms import RegistrarPacienteForm, VerPacienteForm, ModificarPacienteForm, AgregarEntradaForm, VerEntradaForm
from django.contrib import messages
from .models import Paciente, Entrada
# Create your views here.


def registrar_paciente(request):
    form = RegistrarPacienteForm()

    if request.method == 'POST':
        form = RegistrarPacienteForm(request.POST)
        if form.is_valid():
            form.save()
            form = RegistrarPacienteForm()
            messages.success(request, 'Paciente registrado exitosamente')
        else:
            messages.error(request, 'No se pudo registrar el paciente')

    contexto = {'form': form}
    return render(request, 'paciente/registrar_paciente.html', contexto)


def consultar_paciente(request):
    pacientes = list(Paciente.objects.all())
    contexto = {'pacientes': pacientes}
    return render(request, 'paciente/consultar_paciente.html', contexto)


def ver_paciente(request, id_paciente):
    paciente = Paciente.objects.get(identificacion=id_paciente)
    form = VerPacienteForm(instance=paciente)
    contexto = {'form': form, 'paciente': paciente}
    return render(request, 'paciente/ver_paciente.html', contexto)


def modificar_paciente(request, id_paciente):
    paciente = Paciente.objects.get(identificacion=id_paciente)

    if request.method == "POST":
        form = ModificarPacienteForm(request.POST, instance=paciente)

        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente modificado exitosamente')
            return redirect(consultar_paciente)

        else:
            messages.error(request, 'No se pudo modificar el paciente')

    else:
        form = ModificarPacienteForm(instance=paciente)

    contexto = {'form': form, 'paciente': paciente}
    return render(request, 'paciente/modificar_paciente.html', contexto)


def agregar_evolucion_diaria(request):
    form = AgregarEntradaForm()
    if request.method == 'POST':
        form = AgregarEntradaForm(request.POST)
        if form.is_valid():
            form.save()
            form = AgregarEntradaForm()
            messages.success(request, 'Paciente registrado exitosamente')
        else:
            messages.error(request, 'No se pudo registrar el paciente')

    contexto = {'form': form}
    return render(request, 'paciente/agregar_evolucion_diaria.html', contexto)


def consultar_evolucion_diaria(request):
    form = VerEntradaForm()

    contexto = {'form': form}
    return render(request, 'paciente/consultar_evolucion_diaria.html', contexto)


def get_evo_diaria_ajax(request):

    fechas = request.GET.get('rango_fecha')
    fecha_inicial = fechas[6] + fechas[7] + fechas[8] + fechas[9] + "-" + fechas[0] + fechas[1] + "-" + fechas[3] \
                                                                                                + fechas[4]
    fecha_final = fechas[19] + fechas[20] + fechas[21] + fechas[22] + "-" + fechas[13] + fechas[14] + "-" + fechas[16] \
                                                                                                    + fechas[17]
    id_paciente = request.GET.get('id_paciente')
    paciente = Paciente.objects.get(identificacion=id_paciente)
    entradas_paciente = Entrada.objects.filter(paciente=paciente, fecha__range=[fecha_inicial, fecha_final])
    datos = []
    for entrada in entradas_paciente:
        temporal = {
            'fecha': str(entrada.fecha),
            'hora': str("%02d" % (entrada.hora.hour,)) + ":" + str("%02d" % (entrada.hora.minute,)) + ":"
            + str("%02d" % (entrada.hora.second,)),
            'descripcion': entrada.descripcion
        }
        datos.append(temporal)
    datos_json = json.dumps(datos)
    return JsonResponse(datos_json, safe=False)
