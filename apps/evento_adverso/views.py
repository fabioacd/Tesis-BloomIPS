from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import json
from .forms import AgregarImplicadoEventoForm

def index(request):
    return render(request, 'evento_adverso/index.html')

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

            messages.success(request, 'se agregó el implicado al  evento adverso')
            return redirect(agregar_implicado_evento_adverso)
        else:
            print(form_crear_implicado.errors)
            messages.error(request, 'Error al registrar el implicado, intente nuevamente')


    contexto = {'form_crear_implicado': form_crear_implicado}
    return render(request, 'implicado/agregar_implicado_evento_adverso.html', contexto)