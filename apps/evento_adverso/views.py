from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import json
from .forms import AgregarImplicadoEventoForm, ModificarImplicadoEventoAdversoForm, AgregarEventoAdversoForm, ModificarEventoAdversoForm
from .models import ImplicadoEvento, EventoAdverso

def index(request):
    return render(request, 'evento_adverso/index.html')

#---------------------IMPLICADO A EVENTO ADVERSO-----------------------------------------------------

def agregar_implicado_evento_adverso(request):
    form_crear_implicado = AgregarImplicadoEventoForm()

    if request.method == 'POST':

        # PARA OBTENER DE LA BASE DE DATOS
        # id_implicado = request.POST.get('id_implicado',None)
        # instancia = None
        # if id_implicado:
        #     try:
        #         instancia = ImplicadoEvento.objects.get(id_implicado=id_implicado)
        #         form_crear_implicado = AgregarImplicadoEventoForm(instance=instancia)
        #         return render(request, 'implicado/agregar_implicado_evento_adverso.html', {'form_crear_implicado': form_crear_implicado})
        #     except ImplicadoEvento.DoesNotExist:
        #         pass


        form_crear_implicado = AgregarImplicadoEventoForm(request.POST)#, instance=instancia)

        if form_crear_implicado.is_valid():

            form_crear_implicado.save()

            messages.success(request, 'Implicado agregado exitosamente')
            return redirect(agregar_implicado_evento_adverso)
        else:
            print(form_crear_implicado.errors)
            messages.error(request, 'No se pudo registrar el implicado')


    contexto = {'form_crear_implicado': form_crear_implicado}
    return render(request, 'implicado/agregar_implicado_evento_adverso.html', contexto)

def modificar_implicado_evento_adverso(request, id_implicado):
    implicado = ImplicadoEvento.objects.get(id_implicado = id_implicado)

    if request.method == 'POST':
        form = ModificarImplicadoEventoAdversoForm(request.POST, instance = implicado)

        if form.is_valid():
            form.save()
            form = ModificarImplicadoEventoAdversoForm(instance=implicado)
            messages.success(request, 'Implicado modificado exitosamente')
            return redirect(consultar_implicados_evento_adverso)
        else:
            messages.error(request, 'No se pudo modificar el implicado')

    else:
        form = ModificarImplicadoEventoAdversoForm(instance = implicado)

    contexto = {'form': form, 'implicado': implicado}
    return render(request,'implicado/modificar_implicado_evento_adverso.html', contexto)

def consultar_implicados_evento_adverso(request):
    implicados = list(ImplicadoEvento.objects.all())
    contexto = {'implicados': implicados}
    return render(request, 'implicado/consultar_implicado_evento_adverso.html', contexto)


#---------------------EVENTO ADVERSO-----------------------------------------------------

def agregar_evento_adverso(request):
    form_evento_adverso = AgregarEventoAdversoForm()
    if request.method == 'POST':
        form_evento_adverso = AgregarEventoAdversoForm(request.POST)
        if form_evento_adverso.is_valid():
            form_evento_adverso.save()
            messages.success(request, 'se agregó el evento adverso')
            return redirect('consultar_evento')
        else:
            print(form_evento_adverso.errors)
            messages.error(request, 'Error al registrar el evento adverso, intente nuevamente')

    contexto = {'form_evento_adverso':form_evento_adverso}
    return render(request,'evento_adverso/agregar_evento_adverso.html', contexto)

def consultar_evento(request):
    eventos = list(EventoAdverso.objects.all())
    contexto = {'eventos': eventos}
    return render(request, 'evento_adverso/consultar_evento_adverso.html', contexto)

def modificar_evento(request, id_evento):
    evento = EventoAdverso.objects.get(id = id_evento)

    if request.method == 'POST':
        form = ModificarEventoAdversoForm(request.POST, instance = evento)

        if form.is_valid():
            form.save()
            messages.success(request, 'Evento modificado exitosamente')
            return redirect(consultar_evento)
        else:
            messages.error(request, 'No se pudo modificar el evento')

    else:
        form = ModificarEventoAdversoForm(instance = evento)

    contexto = {'form': form, 'evento': evento}
    return render(request,'evento_adverso/modificar_evento_adverso.html', contexto)
