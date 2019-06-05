import datetime
import csv
import json
import magic
import mimetypes
import unidecode
from datetime import date
from django.core import serializers
from io import StringIO
from django.db import transaction, IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from apps.antecedentes.views import registrar_antecedentes_gestacionales, registrar_antecedentes_personales
from apps.empleado.models import Empleado, Area
from utils.utils import check_cargos, convertir_a_pdf
from .forms import RegistrarPacienteForm, VerPacienteForm, ModificarPacienteForm, AgregarEntradaForm, VerEntradaForm, \
    ModificarEntradaForm, CargarCie10Form, AgregarArchivosForm
from .models import Paciente, Entrada, DiagnosticoCie10, ArchivosPaciente
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.urls import reverse_lazy
from django.db.models import Q


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Auxiliar administrativo']))
def registrar_paciente(request):
    form = RegistrarPacienteForm()

    if request.method == 'POST':
        form = RegistrarPacienteForm(request.POST, request.FILES)
        '''if form.is_bound:
            form.fields['diagnosticos_cie10'].queryset = DiagnosticoCie10.objects.all()'''
        if form.is_valid():
            paciente = form.save()
            messages.success(request, 'Paciente registrado exitosamente')
            if request.POST.get("save_and_records") and paciente.tipo_paciente == 'Infante':
                return redirect(registrar_antecedentes_gestacionales)
            elif request.POST.get("save_and_records"):
                return redirect(registrar_antecedentes_personales)
            form = RegistrarPacienteForm()
        else:
            print(form.errors)
            messages.error(request, 'No se pudo registrar el paciente')

    contexto = {'form': form}
    return render(request, 'paciente/registrar_paciente.html', contexto)


@login_required
def consultar_paciente(request):
    return render(request, 'paciente/consultar_paciente.html')


class ajax_filtro_consultar_paciente(BaseDatatableView):
    # The model we're going to show
    model = Paciente

    # define the columns that will be returned
    columns = ['identificacion', 'nombre', 'apellido', 'email', 'celular', 'eps', 'estado', 'modificar']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['identificacion', 'nombre', 'apellido', 'email', 'celular', 'eps', 'estado', 'modificar']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 100

    def render_column(self, row, column):
        paciente = row
        cargo_usuario = self.request.user.cargo
        opciones = []
        if column == 'modificar':
            # Siempre está presente el botón 'Ver paciente'
            opciones.append({
                'texto_boton': 'Ver',
                'url': reverse_lazy('ver_paciente', args=[paciente.id]),
                'color': 'bg-olive'
            })
            # Validación botón 'Modificar'
            if cargo_usuario != "Terapeuta":
                opciones.append({
                    'texto_boton': 'Modificar',
                    'url': reverse_lazy('modificar_paciente', args=[paciente.id]),
                    'color': 'btn-primary'
                })
            return opciones
        return super(ajax_filtro_consultar_paciente, self).render_column(row, column)

    def get_initial_queryset(self):
        return Paciente.objects.all()

    def filter_queryset(self, qs):
        if not self.pre_camel_case_notation:
            search = self._querydict.get('search[value]', None)
            col_data = self.extract_datatables_column_data()
            q = Q()
            for col_no, col in enumerate(col_data):
                column_name = self.columns[col_no].replace('.', '__')
                if hasattr(self.model, column_name):
                    column_name = column_name.replace(' ', '')
                    if search and col['searchable']:
                        realizar_busqueda_base = True
                        if column_name == 'eps':
                            column_name = 'eps__nombre'
                        if realizar_busqueda_base:
                            q |= Q(**{'{0}__icontains'.format(column_name): search})
                    if col['search.value']:
                        if column_name == "eps":
                            eps_filtrada = col['search.value'].lower()
                            qs = qs.filter(eps__nombre__icontains=eps_filtrada)
                        if column_name == "estado":
                            estado_filtrado = col['search.value'].lower()
                            qs = qs.filter(estado__icontains=estado_filtrado)
            qs = qs.filter(q)
        return qs


@login_required
def ver_paciente(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    form = VerPacienteForm(instance=paciente)
    contexto = {'form': form, 'paciente': paciente}
    return render(request, 'paciente/ver_paciente.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Auxiliar administrativo']))
def modificar_paciente(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)

    if request.method == "POST":
        form = ModificarPacienteForm(request.POST, request.FILES, instance=paciente)
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


@login_required
@user_passes_test(check_cargos(['Administrador']))
def modificar_evolucion_diaria(request, id_entrada):
    entrada = get_object_or_404(Entrada, id=id_entrada)

    if request.method == "POST":
        form = ModificarEntradaForm(request.POST, instance=entrada)

        if form.is_valid():
            form.save()
            messages.success(request, "Entrada modificada exitosamente")
            return redirect(consultar_evolucion_diaria)

        else:
            messages.error(request, "No se pudo modificar la entrada")

    else:
        form = ModificarEntradaForm(instance=entrada)

    contexto = {'form': form}
    return render(request, 'paciente/modificar_evolucion_diaria.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Terapeuta']))
def agregar_evolucion_diaria(request):
    form = AgregarEntradaForm(usuario=request.user)
    if request.method == 'POST':
        form = AgregarEntradaForm(request.POST, usuario=request.user)
        if form.is_valid():
            entrada = form.save(commit=False)
            entrada.empleado = request.user
            entrada.hora = datetime.datetime.now()
            entrada.fecha = date.today()
            entrada.save()
            messages.success(request, 'Entrada registrada exitosamente')
            return redirect('agregar_evolucion_diaria')
        else:
            messages.error(request, 'No se pudo registrar la entrada')

    contexto = {'form': form}
    return render(request, 'paciente/agregar_evolucion_diaria.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Terapeuta', 'Auxiliar administrativo']))
def consultar_evolucion_diaria(request):
    form = VerEntradaForm(usuario=request.user)

    if request.method == 'POST':
        # Todo lo relacionado para pdf de Historia Clínica
        id_paciente = request.POST.get('paciente')

        fecha = request.POST.get('fechas[value]').replace(" ", "").split('-')
        fecha_inicial = datetime.datetime.strptime(fecha[0], '%m/%d/%Y').strftime('%Y-%m-%d')
        fecha_final = datetime.datetime.strptime(fecha[1], '%m/%d/%Y').strftime('%Y-%m-%d')
        paciente = get_object_or_404(Paciente, id=id_paciente)
        fecha_edad = datetime.datetime.now()
        edad_paciente = int(fecha_edad.year) - int(paciente.fecha_nacimiento.year) - (
                (fecha_edad.month, fecha_edad.day) < (paciente.fecha_nacimiento.month, paciente.fecha_nacimiento.day))
        entradas_paciente = Entrada.objects.filter(paciente=paciente, fecha__range=[fecha_inicial, fecha_final])

        if entradas_paciente:
            if request.user.cargo != 'Terapeuta':
                nombre_archivo = str(fecha_inicial) + '-a-' + str(fecha_final) + '-HC-' + \
                                 str(paciente.eps) + '-' + paciente.nombre + '-' + paciente.apellido
                nombre_archivo = unidecode.unidecode(nombre_archivo)
                contexto = {'paciente': paciente, 'edad_paciente': edad_paciente,
                            'entradas_paciente': entradas_paciente}
                pdf = convertir_a_pdf('pdf/historia_clinica.html', nombre_archivo, contexto)
                return pdf
            else:
                messages.warning(request, 'No tiene permiso para generar la historia clínica.')
                return redirect(consultar_evolucion_diaria)
        else:
            messages.warning(request, 'El paciente no posee entradas en el rango de fechas seleccionado')
            return redirect(consultar_evolucion_diaria)

    contexto = {'form': form}
    return render(request, 'paciente/consultar_evolucion_diaria.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Terapeuta', 'Auxiliar administrativo']))
def get_pacientes_entradas_ajax(request):
    id_area = request.GET.get('area')
    empleado = request.user
    fechas = request.GET.get('rango_fecha')
    fecha_inicial = fechas[6] + fechas[7] + fechas[8] + fechas[9] + "-" + fechas[0] + fechas[1] + "-" + fechas[3] \
                    + fechas[4]
    fecha_final = fechas[19] + fechas[20] + fechas[21] + fechas[22] + "-" + fechas[13] + fechas[14] + "-" + fechas[16] \
                  + fechas[17]
    pacientes_entrada = Paciente.objects.filter(estado='Activo',
                                                entradas_paciente__fecha__range=[fecha_inicial, fecha_final]).distinct()
    if id_area != 'all':
        area = get_object_or_404(Area, id=id_area)
        pacientes_entrada = pacientes_entrada.filter(entradas_paciente__area=area)
    if empleado.cargo == 'Terapeuta':
        area = empleado.area.all()
        pacientes_entrada = pacientes_entrada.filter(entradas_paciente__area__in=area, entradas_paciente__empleado=empleado)

    list(pacientes_entrada)

    datos = []
    for paciente in pacientes_entrada:
        temp = {
            'id': paciente.id,
            'identificacion': paciente.identificacion,
            'nombre': paciente.nombre,
            'apellido': paciente.apellido
        }
        datos.append(temp)
    datos_json = json.dumps(datos)
    return JsonResponse(datos_json, safe=False)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Terapeuta']))
def get_entradas_dia_ajax(request):
    id_paciente = request.GET.get('id_paciente')

    paciente = get_object_or_404(Paciente, id=id_paciente)

    fecha = datetime.datetime.now()
    entradas = list(Entrada.objects.filter(fecha=fecha, paciente=paciente))
    datos = []
    edad = int(fecha.year) - int(paciente.fecha_nacimiento.year) - (
                (fecha.month, fecha.day) < (paciente.fecha_nacimiento.month, paciente.fecha_nacimiento.day))
    temp = {
        'edad_paciente': edad,
        'enfermedad': paciente.enfermedad_actual
    }
    datos.append(temp)
    for entrada in entradas:
        temp = {
            'empleado': entrada.empleado.first_name + ' ' + entrada.empleado.last_name,
            'hora': str("%02d" % (entrada.hora.hour,)) + ":" + str("%02d" % (entrada.hora.minute,)) + ":"
                    + str("%02d" % (entrada.hora.second,)),
            'descripcion': entrada.descripcion,
            'area': entrada.area.nombre

        }
        datos.append(temp)
    datos_json = json.dumps(datos)
    return JsonResponse(datos_json, safe=False)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Terapeuta', 'Auxiliar administrativo']))
def get_evo_diaria_ajax(request):
    fechas = request.GET.get('rango_fecha')
    fecha_inicial = fechas[6] + fechas[7] + fechas[8] + fechas[9] + "-" + fechas[0] + fechas[1] + "-" + fechas[3] \
                    + fechas[4]
    fecha_final = fechas[19] + fechas[20] + fechas[21] + fechas[22] + "-" + fechas[13] + fechas[14] + "-" + fechas[16] \
                  + fechas[17]
    id_paciente = request.GET.get('id_paciente')
    id_area = request.GET.get('area')
    paciente = get_object_or_404(Paciente, id=id_paciente)

    if id_area != 'all':
        area = get_object_or_404(Area, id=id_area)

        entradas_paciente = Entrada.objects.filter(paciente=paciente, fecha__range=[fecha_inicial, fecha_final],
                                                   area=area)
    else:
        area = Area.objects.all()
        entradas_paciente = Entrada.objects.filter(paciente=paciente, fecha__range=[fecha_inicial, fecha_final],
                                                   area__in=area)

    datos = []
    for entrada in entradas_paciente:
        temporal = {
            'id_ent': str(entrada.id),
            'area': entrada.area.nombre,
            'fecha': str(entrada.fecha),
            'hora': str("%02d" % (entrada.hora.hour,)) + ":" + str("%02d" % (entrada.hora.minute,)) + ":"
                    + str("%02d" % (entrada.hora.second,)),
            'descripcion': entrada.descripcion,
            'emp_nombre': entrada.empleado.first_name,
            'emp_apellido': entrada.empleado.last_name
        }
        datos.append(temporal)
    datos_json = json.dumps(datos)
    return JsonResponse(datos_json, safe=False)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Terapeuta']))
def agregar_archivo_paciente(request):
    form = AgregarArchivosForm()
    archivos = serializers.serialize("json", ArchivosPaciente.objects.all())
    if request.method == 'POST':
        form = AgregarArchivosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Archivo agregado exitosamente')
            return redirect(agregar_archivo_paciente)
        else:
            messages.error(request, 'No se pudo agregar el archivo')

    contexto = {'form': form, 'archivos': archivos}
    return render(request, 'paciente/agregar_archivo_paciente.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Terapeuta']))
def eliminar_archivo_paciente_ajax(request):
    archivo = get_object_or_404(ArchivosPaciente, pk=request.GET.get('id_archivo'))
    archivo.delete()
    datos_json = json.dumps([{'eliminado': True}])
    return JsonResponse(datos_json, safe=False)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Auxiliar administrativo']))
def get_diagnosticos_ajax(request):
    # TODO
    codigo_palabra = request.GET.get('codigo_palabra')
    diagnosticos = DiagnosticoCie10.objects.filter(
        Q(descripcion__icontains=codigo_palabra) | Q(id_diagnostico__icontains=codigo_palabra))
    datos = []
    for diag in diagnosticos:
        temp = {
            'id': diag.id_diagnostico,
            'descripcion': diag.descripcion,
        }
        datos.append(temp)
    datos_json = json.dumps(datos)
    return JsonResponse(datos_json, safe=False)


@login_required
@user_passes_test(check_cargos(['Administrador']))
def carga_masiva_cie10(request):
    form = CargarCie10Form()
    success_exit = True
    if request.method == 'POST':
        form = CargarCie10Form(request.POST, request.FILES)
        if form.is_valid():
            csv_string = request.FILES['carga_cie10'].read().decode(encoding="ISO-8859-1")
            csv_file = StringIO(csv_string)
            file_readed = csv.reader(csv_file, delimiter=",", quotechar='"')
            linea = 0
            try:
                with transaction.atomic():
                    for valores in file_readed:
                        if linea == 0:
                            if (valores[0] and valores[1] and valores[2]) != '':
                                if (valores[0] != 'id10') or (valores[1] != 'dec10') or (
                                        valores[2].rstrip('\r\n') != 'grp10'):
                                    messages.error(request, "Las cabeceras tienen nombres incorrectos.")
                                    success_exit = False
                                    break
                            else:
                                messages.error(request, "Las cabeceras de las columnas son obligatorias.")
                                success_exit = False
                                break

                        if linea != 0:
                            if (valores[0] and valores[1]) != '':
                                if valores[0].find('|') == -1:
                                    cod_cie10 = valores[0]
                                    desc_cie10 = valores[1]
                                    if DiagnosticoCie10.objects.filter(id_diagnostico=cod_cie10).exists():
                                        diagnostico_mod = DiagnosticoCie10.objects.get(id_diagnostico=cod_cie10)
                                        diagnostico_mod.descripcion = desc_cie10
                                        diagnostico_mod.save()
                                    else:
                                        DiagnosticoCie10.objects.create(id_diagnostico=cod_cie10,
                                                                        descripcion=desc_cie10)
                            else:
                                messages.error(request, "Error en la línea " + str(linea)
                                               + " del archivo. Los campos id10 y dec10 son obligatorios.")
                                success_exit = False
                                break
                        linea += 1
                    if success_exit:
                        messages.success(request, "Archivo cargado con éxito.")
                    elif not success_exit:
                        messages.error(request, "El archivo no ha podido ser cargado.")
            except IntegrityError:
                messages.error(request,
                               'El archivo no ha podido ser cargado debido a un error en la base de datos.')
            except IndexError:
                messages.error(request,
                               'El archivo no ha podido ser cargado. Asegúrese de que contenga las columnas '
                               'requeridas.')

        else:
            messages.error(request, 'Por favor ingrese un archivo csv.')
    contexto = {'form': form}
    return render(request, 'paciente/cargar_cie10.html', contexto)
