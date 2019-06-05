import calendar
import datetime
import json
from datetime import date
from html import escape
import unidecode

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Count, F
from django.db.models.functions import datetime
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django_datatables_view.base_datatable_view import BaseDatatableView

from .forms import AgregarEmpleadoForm, AgregarEpsForm, AgregarAreaForm, ModificarAreaForm, \
    ModificarEmpleadoForm, AgregarResumenForm, AgregarResumenEspecificoForm, ModificarEpsForm, \
    ModificarResumenForm, InformacionPersonalForm, VerResumenForm, VerPacientesInformeMensualForm
from django.contrib import messages
from .models import Area, Resumen, Empleado
from apps.paciente.models import Entrada, Paciente, Eps
from django.shortcuts import redirect
from utils.utils import convertir_a_pdf, rango_fechas_informe_mensual, check_cargos, nombre_mes


# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'empleado/dashboard.html')


@login_required
def informacion_personal(request):
    empleado = get_object_or_404(Empleado, username=request.user.username)

    if request.method == 'POST':
        form = InformacionPersonalForm(request.POST, request.FILES, instance=empleado, usuario=empleado)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario modificado exitosamente')
            return redirect(dashboard)
        else:
            messages.error(request, 'No se pudo modificar el empleado')
    else:
        form = InformacionPersonalForm(instance=empleado)

    contexto = {'form': form}
    return render(request, 'empleado/informacion_personal.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador']))
def agregar_empleado(request):
    form = AgregarEmpleadoForm()
    if request.method == 'POST':
        form = AgregarEmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form.save_m2m()
            messages.success(request, 'Empleado registrado exitosamente')
            return redirect(consultar_empleado)
        else:
            messages.error(request, 'No se pudo registrar el empleado')
    contexto = {'form': form}
    return render(request, 'empleado/agregar_empleado.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador']))
def consultar_empleado(request):
    empleados = list(Empleado.objects.all())
    contexto = {'empleados': empleados}
    return render(request, 'empleado/consultar_empleado.html', contexto)

class ajax_filtro_consultar_empleado(BaseDatatableView):
    model = Empleado
    columns = ['username', 'first_name', 'last_name', 'cargo', 'area', 'email', 'modificar']
    order_columns = ['username', 'first_name', 'last_name', 'cargo', 'area', 'email', '']
    max_display_length = 100

    def render_column(self, row, column):
        empleado = row
        cargo_usuario = self.request.user.cargo
        opciones = []
        if column == 'modificar':
            # Validación botón 'Modificar'
            if cargo_usuario == "Coordinador":
                if empleado.cargo  == 'Administrador' or empleado.cargo == 'Coordinador':
                    opciones.append({
                        'texto_boton': 'Modificar',
                        'url': 'javascript:;',
                        'color': 'btn-primary'
                    })
                else:
                    opciones.append({
                        'texto_boton': 'Modificar',
                        'url': reverse_lazy('modificar_empleado', args=[empleado.username]),
                        'color': 'btn-primary'
                    })
            else:
                opciones.append({
                    'texto_boton': 'Modificar',
                    'url': reverse_lazy('modificar_empleado', args=[empleado.username]),
                    'color': 'btn-primary'
                })
            return opciones

        if column == 'area':
            for area in empleado.area.all():
                opciones.append(area.nombre)
            return opciones

        return super(ajax_filtro_consultar_empleado, self).render_column(row, column)

    def get_initial_queryset(self):
        return Empleado.objects.all()

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
                        if column_name == 'area':
                            column_name = 'area__nombre'
                        q |= Q(**{'{0}__icontains'.format(column_name): search})
            qs = qs.filter(q).distinct()
        return qs

@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador']))
def modificar_empleado(request, id_empleado):
    empleado = get_object_or_404(Empleado, username=id_empleado)

    if request.user.cargo == 'Coordinador' and (empleado.cargo == 'Administrador'
                                                or empleado.cargo == 'Coordinador'):
        messages.warning(request, 'No tiene permiso para modificar Coordinadores o Administradores.')
        return redirect(consultar_empleado)
    else:
        if request.method == 'POST':
            form = ModificarEmpleadoForm(request.POST, request.FILES, instance=empleado)
            if form.is_valid():
                form.save()
                form.save_m2m()
                messages.success(request, 'Usuario modificado exitosamente')
                return redirect(consultar_empleado)
            else:
                messages.error(request, 'No se pudo modificar el empleado')
        else:
            form = ModificarEmpleadoForm(instance=empleado)
        contexto = {'form': form, 'empleado': empleado}
        return render(request, 'empleado/modificar_empleado.html', contexto)


# --------------------AREA-----------------------------------------------------
@login_required
@user_passes_test(check_cargos(['Administrador']))
def agregar_area(request):
    form = AgregarAreaForm()
    if request.method == 'POST':
        form = AgregarAreaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Área registrada exitosamente')
            return redirect(consultar_area)
        else:
            messages.error(request, 'No se pudo registrar el área')
    # elif  not request.user.is_authenticated:
    # return redirect('login')
    contexto = {'form': form}
    return render(request, 'area/agregar_area.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador']))
def consultar_area(request):
    return render(request, 'area/consultar_area.html')


class ajax_filtro_consultar_area(BaseDatatableView):
    # The model we're going to show
    model = Area

    # define the columns that will be returned
    columns = ['nombre', 'tipo', 'descripcion', 'modificar']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['nombre', 'tipo', 'descripcion', 'modificar']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 100

    def render_column(self, row, column):
        area = row
        if column == 'modificar':
            return reverse_lazy('modificar_area', args=[area.id])
        return super(ajax_filtro_consultar_area, self).render_column(row, column)

    def get_initial_queryset(self):
        return Area.objects.all()

    def filter_queryset(self, qs):
        if not self.pre_camel_case_notation:
            search = self._querydict.get('search[value]', None)
            col_data = self.extract_datatables_column_data()
            q = Q()
            for col_no, col in enumerate(col_data):
                if hasattr(self.model, self.columns[col_no].replace('.', '__')):
                    if search and col['searchable']:
                        q |= Q(**{'{0}__icontains'.format(self.columns[col_no].replace('.', '__')): search})
            qs = qs.filter(q)
        return qs


@login_required
@user_passes_test(check_cargos(['Administrador']))
def modificar_area(request, id_area):
    area = get_object_or_404(Area, id=id_area)

    if request.method == 'POST':
        form = ModificarAreaForm(request.POST, instance=area)

        if form.is_valid():
            form.save()
            messages.success(request, 'Área modificada exitosamente')
            return redirect(consultar_area)
        else:
            messages.error(request, 'No se pudo modificar el área')

    else:
        form = ModificarAreaForm(instance=area)

    contexto = {'form': form}
    return render(request, 'area/modificar_area.html', contexto)


# ----------------------INFORME MENSUAL--------------------------------------------
@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Terapeuta']))
def agregar_resumen(request):
    form = AgregarResumenForm(usuario=request.user)
    if request.method == 'POST':
        form = AgregarResumenForm(request.POST, usuario=request.user)
        if form.is_valid():
            resumen = form.save(commit=False)
            resumen.empleado = request.user
            resumen.hora = datetime.datetime.now()
            resumen.fecha = date.today()
            resumen.save()
            messages.success(request, 'Informe mensual registrado exitosamente')
            return redirect(consultar_resumen)
        else:
            messages.error(request, 'No se pudo registrar el informe mensual')
    contexto = {'form': form}
    return render(request, 'resumen/agregar_resumen.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador']))
def agregar_resumen_especifico(request, id_paciente, nombre_area, id_terapeuta, fecha):
    fecha = fecha.split('-')
    month = int(fecha[0])
    year = int(fecha[1])
    dia_final = calendar.monthrange(year, month)[1]
    fecha_inicial = datetime.datetime(year, month, 1)
    fecha_final = datetime.datetime(year, month, dia_final)
    area = get_object_or_404(Area, nombre=nombre_area)
    paciente = get_object_or_404(Paciente, identificacion=id_paciente)
    if id_terapeuta != 'NO':
        terapeutas = Empleado.objects.filter(username=id_terapeuta)
    else:
        terapeutas = Empleado.objects.filter(entradas_empleado__fecha__range=[fecha_inicial, fecha_final],
                                      entradas_empleado__paciente=paciente, entradas_empleado__area=area).distinct()

    entradas = list(Entrada.objects.filter(paciente=paciente, fecha__range=[fecha_inicial, fecha_final], area=area))
    datos_entradas = []
    for entrada in entradas:
        temporal = {
            'fecha': str(entrada.fecha),
            'empleado': (entrada.empleado.first_name + ' ' + entrada.empleado.last_name),
            'area': str(entrada.area),
            'hora': str("%02d" % (entrada.hora.hour,)) + ":" + str("%02d" % (entrada.hora.minute,)) + ":"
                    + str("%02d" % (entrada.hora.second,)),
            'descripcion': entrada.descripcion
        }
        datos_entradas.append(temporal)
    if request.method == 'POST':
        form = AgregarResumenEspecificoForm(request.POST, empleados=terapeutas)
        if form.is_valid():
            if Resumen.objects.filter(paciente=paciente, fecha__range=[fecha_inicial, fecha_final], area=area).exists():
                messages.error(request, 'Ya existe un informe mensual para el paciente indicado.')
                return render(request, 'resumen/consultar_resumen.html')
            else:
                resumen = form.save(commit=False)
                resumen.hora = datetime.datetime.now()
                resumen.fecha = fecha_final
                resumen.area = area
                resumen.paciente = paciente
                resumen.save()
                messages.success(request, 'Informe mensual registrado exitosamente')
                return redirect(consultar_resumen)
        else:
            messages.error(request, 'No se pudo registrar el informe mensual')
    else:
        form = AgregarResumenEspecificoForm(empleados=terapeutas)
    mes = nombre_mes(fecha_inicial.strftime("%B"))

    content_informe = {'paciente': paciente, 'area': area, 'mes': mes}
    contexto = {'form': form, 'entradas': datos_entradas, 'content_informe': content_informe}
    return render(request, 'resumen/agregar_resumen_especifico.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Terapeuta']))
def consultar_resumen(request):
    return render(request, 'resumen/consultar_resumen.html')


class ajax_filtro_consultar_resumen(BaseDatatableView):
    # The model we're going to show
    model = Resumen

    # define the columns that will be returned
    columns = ['empleado', 'paciente', 'fecha', 'area', 'revisado', 'acciones']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['empleado', 'paciente', 'fecha', 'area', 'revisado', '']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 100

    def render_column(self, row, column):
        resumen = row
        usuario = self.request.user
        if column == 'acciones':
            acciones = []
            if resumen.revisado == False:
                if usuario.cargo in ['Administrador', 'Coordinador'] or usuario == resumen.empleado:
                    acciones.append({
                        "opcion": "modificar_resumen",
                        "url": reverse_lazy('modificar_resumen', args=[resumen.id])
                    })
                else:
                    acciones.append({
                        "opcion": "ver_resumen",
                        "url": reverse_lazy('ver_resumen', args=[resumen.id])
                    })
            else:
                if usuario.cargo in ['Administrador', 'Coordinador']:
                    acciones.append({
                        "opcion": "modificar_resumen",
                        "url": reverse_lazy('modificar_resumen', args=[resumen.id])
                    })
                else:
                    acciones.append({
                        "opcion": "ver_resumen",
                        "url": reverse_lazy('ver_resumen', args=[resumen.id])
                    })
            return acciones
        if column == 'revisado':
            if resumen.revisado:
                return "Revisado"
            else:
                return "Sin revisar"
        if column == 'fecha':
            return resumen.get_mes_anio()
        return super(ajax_filtro_consultar_resumen, self).render_column(row, column)

    def get_initial_queryset(self):
        return Resumen.objects.all()

    def filter_queryset(self, qs):
        if not self.pre_camel_case_notation:
            search = self._querydict.get('search[value]', None)
            col_data = self.extract_datatables_column_data()
            q = Q()
            for col_no, col in enumerate(col_data):
                column_name = self.columns[col_no].replace('.', '__')
                if hasattr(self.model, column_name):
                    column_name = column_name.replace(' ', '')
                    #Filtro general
                    if search and col['searchable']:
                        realizar_busqueda_base = True
                        if column_name == 'revisado':
                            if search.lower() in "revisado":
                                search = True
                            elif search.lower() in "sin revisar":
                                search = False
                        if column_name == 'area':
                            realizar_busqueda_base = False
                            q |= Q(**{'{0}__icontains'.format('area__nombre'): search})
                        if column_name == 'empleado':
                            realizar_busqueda_base = False
                            q |= Q(**{'{0}__icontains'.format('empleado__first_name'): search}) | Q(**{'{0}__icontains'.format('empleado__last_name'): search}) | Q(**{'{0}__icontains'.format('empleado__username'): search})
                        if column_name == 'paciente':
                            realizar_busqueda_base = False
                            q |= Q(**{'{0}__icontains'.format('paciente__nombre'): search}) | Q(**{'{0}__icontains'.format('paciente__apellido'): search}) | Q(
                                **{'{0}__icontains'.format('paciente__identificacion'): search})
                        if realizar_busqueda_base:
                            q |= Q(**{'{0}__icontains'.format(column_name): search})
                    #Filtros por columnas
                    if col['search.value']:
                        if column_name == "area":
                            area_filtrada = col['search.value'].lower()
                            qs = qs.filter(area__nombre__icontains=area_filtrada)
                        if column_name == "fecha":
                            fecha_filtrada = col['search.value'].lower()
                            qs = qs.filter(fecha__icontains=fecha_filtrada)
                        if column_name == "revisado":
                            revisado_filtrado = col['search.value'].lower()
                            revisado_bool = False
                            if revisado_filtrado == 'revisado':
                                revisado_bool = True
                            qs = qs.filter(revisado=revisado_bool)

            qs = qs.filter(q)
        return qs


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador']))
def consultar_informe_area(request):
    form = VerPacientesInformeMensualForm()
    contexto = {'form': form}
    return render(request, 'resumen/consultar_informe_area.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador']))
def consultar_informe_paciente(request):
    titulos = []
    areas = Area.objects.exclude(nombre='Administrativa')
    for area in areas:
        titulos.append(str(area))
    contexto = {'titulos': titulos}
    return render(request, 'resumen/consultar_informe_paciente.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Terapeuta']))
def generar_pdf_informe_mensual(request, id_resumen):
    # Todo lo relacionado para pdf de resumen
    resumen = get_object_or_404(Resumen, id=id_resumen)
    nombre_archivo = 'I mensual - ' + str(resumen.empleado.first_name) + ' ' + str(resumen.empleado.last_name) + \
                     ' - ' + resumen.get_mes() + '/' + str(resumen.fecha.strftime('%Y')) + ' - ' + str(resumen.area) + \
                     ' - ' + str(resumen.paciente.nombre) + ' ' + str(resumen.paciente.apellido)
    contexto = {'resumen': resumen, 'fecha': resumen.get_mes() + '/' + str(resumen.fecha.strftime('%Y'))}
    pdf = convertir_a_pdf('pdf/informe_mensual.html', nombre_archivo, contexto)
    # messages.success(request, 'PDF informe mensual generado exitosamente')
    return pdf


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Terapeuta']))
def modificar_resumen(request, id_resumen):
    resumen = get_object_or_404(Resumen, id=id_resumen)
    usuario = request.user
    if resumen.revisado and usuario.cargo == 'Terapeuta':
        messages.error(request, 'El informe mensual ya ha sido revisado')
        return redirect('consultar_resumen')
    elif resumen.empleado != usuario and usuario.cargo == 'Terapeuta':
        messages.error(request, 'No puede modificar el informe mensual')
        return redirect('consultar_resumen')
    dia_final = calendar.monthrange(resumen.fecha.year, resumen.fecha.month)[1]
    fecha_inicial = datetime.datetime(resumen.fecha.year, resumen.fecha.month, 1)
    fecha_final = datetime.datetime(resumen.fecha.year, resumen.fecha.month, dia_final)
    paciente = resumen.paciente
    entradas = list(
        Entrada.objects.filter(paciente=paciente, fecha__range=[fecha_inicial, fecha_final], area=resumen.area))
    datos_entradas = []
    for entrada in entradas:
        temporal = {
            'fecha': str(entrada.fecha),
            'hora': str("%02d" % (entrada.hora.hour,)) + ":" + str("%02d" % (entrada.hora.minute,)) + ":"
                    + str("%02d" % (entrada.hora.second,)),
            'descripcion': entrada.descripcion
        }
        datos_entradas.append(temporal)
    if request.method == 'POST':
        form = ModificarResumenForm(request.POST, instance=resumen)
        if form.is_valid():
            instancia_resumen = form.save(commit=False)
            if not instancia_resumen.revisado and usuario.cargo == 'Terapeuta' or usuario.cargo != 'Terapeuta':
                instancia_resumen.save()
                messages.success(request, 'Informe mensual modificado exitosamente')
            else:
                messages.error(request, 'El informe mensual ya ha sido revisado')
            return redirect(consultar_resumen)
        else:
            messages.error(request, 'No se pudo modificar el informe mensual')
    else:
        form = ModificarResumenForm(instance=resumen)

    contexto = {'form': form, 'entradas': datos_entradas, 'paciente': paciente}
    return render(request, 'resumen/modificar_resumen.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Terapeuta']))
def ver_resumen(request, id_resumen):
    resumen = get_object_or_404(Resumen, id=id_resumen)
    form = VerResumenForm(instance=resumen)
    contexto = {'form': form, 'resumen': resumen}
    return render(request, 'resumen/ver_resumen.html', contexto)


# -------------------------------EPS--------------------------------------------
@login_required
@user_passes_test(check_cargos(['Administrador']))
def agregar_eps(request):
    form = AgregarEpsForm()
    if request.method == 'POST':
        form = AgregarEpsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Eps registrada exitosamente')
            return redirect(consultar_eps)
        else:
            messages.error(request, 'No se pudo registrar la eps')
    contexto = {'form': form}
    return render(request, 'eps/agregar_eps.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador']))
def modificar_eps(request, nit):
    eps = get_object_or_404(Eps, nit=nit)

    if request.method == 'POST':
        form = ModificarEpsForm(request.POST, instance=eps)

        if form.is_valid():
            form.save()
            messages.success(request, 'EPS modificada exitosamente')
            return redirect(consultar_eps)
        else:
            messages.error(request, 'No se pudo modificar la EPS')

    else:
        form = ModificarEpsForm(instance=eps)

    contexto = {'form': form}
    return render(request, 'eps/modificar_eps.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador']))
def consultar_eps(request):
    return render(request, 'eps/consultar_eps.html')


class ajax_filtro_consultar_eps(BaseDatatableView):
    # The model we're going to show
    model = Eps

    # define the columns that will be returned
    columns = ['nit', 'nombre', 'direccion', 'telefono', 'modificar']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['nit', 'nombre', 'direccion', 'telefono', '']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 100

    def render_column(self, row, column):
        eps = row
        if column == 'modificar':
            return reverse_lazy('modificar_eps', args=[eps.nit])
        return super(ajax_filtro_consultar_eps, self).render_column(row, column)

    def get_initial_queryset(self):
        return Eps.objects.all()

    def filter_queryset(self, qs):
        if not self.pre_camel_case_notation:
            search = self._querydict.get('search[value]', None)
            col_data = self.extract_datatables_column_data()
            q = Q()
            for col_no, col in enumerate(col_data):
                if hasattr(self.model, self.columns[col_no].replace('.', '__')):
                    if search and col['searchable']:
                        q |= Q(**{'{0}__icontains'.format(self.columns[col_no].replace('.', '__')): search})
            qs = qs.filter(q)
        return qs


# --------------------CONSOLIDADO-----------------------------------------------------

@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Auxiliar administrativo']))
def agregar_consolidado(request):
    titulos = []
    areas = Area.objects.exclude(nombre='Administrativa')
    for area in areas:
        titulos.append(str(area))
    contexto = {'titulos': titulos}
    return render(request, 'consolidado/agregar_consolidado.html', contexto)


@login_required
def generar_consolidado(request, id_paciente, fecha, tipo_area):
    try:
        fecha = fecha.split('-')
        month = int(fecha[0])
        year = int(fecha[1])
        dia_final = calendar.monthrange(year, month)[1]
        fecha_inicio = datetime.datetime(year, month, 1)
        fecha_fin = datetime.datetime(year, month, dia_final)
        paciente = get_object_or_404(Paciente, identificacion=id_paciente)
        if tipo_area != 'Todas':
            resumenes_paciente = paciente.resumenes.filter(fecha__range=[fecha_inicio, fecha_fin],
                                                           area__tipo=tipo_area).order_by('area', 'id')
        else:
            resumenes_paciente = paciente.resumenes.filter(fecha__range=[fecha_inicio, fecha_fin]).order_by('area',
                                                                                                            'id')
        # anio_mes_dia_EI_eps_nombre-paciente
        if resumenes_paciente:
            fecha_actual = datetime.datetime.now()
            nombre_archivo = str(fecha_actual.year) + "_" + str(fecha_actual.month) + "_" + str(
                fecha_actual.day) + "_EI_" + str(paciente.eps) + "_" + paciente.nombre + "_" + paciente.apellido
            nombre_archivo = unidecode.unidecode(nombre_archivo)
            contexto = {'resumenes': resumenes_paciente, 'paciente': paciente, 'fecha_inicio': fecha_inicio,
                        'fecha_fin': fecha_fin}
            pdf = convertir_a_pdf('pdf/consolidado_paciente.html', nombre_archivo, contexto)
            return pdf
        else:
            raise Http404
    except Exception:
        raise Http404


# -------------------------LLAMADAS AJAX----------------------------------------
@login_required
def get_entradas_ajax(request):
    fechas = request.GET.get('rango_fecha')
    fecha_inicial = fechas[6] + fechas[7] + fechas[8] + fechas[9] + "-" + fechas[0] + fechas[1] + "-" + fechas[3] + \
                    fechas[4]
    fecha_final = fechas[19] + fechas[20] + fechas[21] + fechas[22] + "-" + fechas[13] + fechas[14] + "-" + fechas[16] + \
                  fechas[17]
    id_paciente = request.GET.get('id_paciente')
    paciente = get_object_or_404(Paciente, id=id_paciente)
    empleado = request.user
    area = request.GET.get('area')
    if area == '':
        entradas_paciente = Entrada.objects.filter(paciente=paciente, fecha__range=[fecha_inicial, fecha_final])
        area = empleado.area.all()
        entradas = list(entradas_paciente.filter(area__in=area))
    else:
        entradas = list(Entrada.objects.filter(paciente=paciente, fecha__range=[fecha_inicial, fecha_final], area=area))
    datos = []
    for entrada in entradas:
        temporal = {
            'fecha': str(entrada.fecha),
            'hora': str("%02d" % (entrada.hora.hour,)) + ":" + str("%02d" % (entrada.hora.minute,)) + ":"
                    + str("%02d" % (entrada.hora.second,)),
            'descripcion': entrada.descripcion,
            'area': entrada.area.nombre,
            'empleado': entrada.empleado.first_name + " " + entrada.empleado.last_name
        }
        datos.append(temporal)
    datosJson = json.dumps(datos)
    return JsonResponse(datosJson, safe=False)


@login_required
def get_pacientes_informe_ajax(request):
    id_area = request.GET.get('area')
    empleado = request.user
    area = get_object_or_404(Area, id=id_area)
    rango_fechas = rango_fechas_informe_mensual()
    pacientes_entrada = Paciente.objects.filter(estado='Activo', entradas_paciente__area=area, entradas_paciente__empleado=empleado,
                                                entradas_paciente__fecha__range=rango_fechas)
    pacientes_resumen = Paciente.objects.exclude(resumenes__fecha__range=[rango_fechas[0], rango_fechas[1]],
                                                 resumenes__area=area)
    pacientes = list(pacientes_resumen.intersection(pacientes_entrada))
    datos = []
    for paciente in pacientes:
        temp = {
            'id': paciente.id,
            'identificacion': paciente.identificacion,
            'nombre': paciente.nombre,
            'apellido': paciente.apellido
        }
        datos.append(temp)
    datosJson = json.dumps(datos)
    return JsonResponse(datosJson, safe=False)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador']))
def consultar_informe_area_ajax(request):
    area_id = request.GET.get('area')
    fecha = request.GET.get('fecha')
    area = get_object_or_404(Area, id=area_id)

    info_con_resumen = []
    info_sin_resumen = []
    if area_id == '' or fecha == '':
        return JsonResponse({'status': False, 'datos': info_sin_resumen}, safe=False)
    else:
        fecha = fecha.split('-')
        month = int(fecha[0])
        year = int(fecha[1])
        dia_final = calendar.monthrange(year, month)[1]
        fecha_inicial = datetime.datetime(year, month, 1)
        fecha_final = datetime.datetime(year, month, dia_final)

        # Resumenes realizados en rango de fechas y área.
        resumenes_realizados = Resumen.objects.filter(fecha__range=[fecha_inicial, fecha_final], area=area_id, paciente__estado='Activo')
        pacientes_resumen = Paciente.objects.exclude(resumenes__fecha__range=[fecha_inicial, fecha_final],
                                                     resumenes__area=area).filter(estado='Activo')

        # Todas las entradas en rango de fecha, por área. Distintct para no traerlas todas
        entradas_paciente_sin_resumen = Entrada.objects.filter(area=area_id, fecha__range=[fecha_inicial, fecha_final],
                                                               paciente__in=pacientes_resumen).distinct(
            'area', 'empleado', 'paciente')

        # Se añaden objetos que constan aquellos paciente CON informe mensual. NO TOCAR, ESTO YA ESTÁ FUNCIONANDO
        for resumen in resumenes_realizados:
            temporal = {
                'paciente': str(resumen.paciente),
                'area': str(resumen.area),
                'terapeuta': str(resumen.empleado),
                'resumen_id': resumen.id,
            }
            info_con_resumen.append(temporal)

        # Se añaden objetos que constan aquellos paciente SIN informe mensual
        for entrada in entradas_paciente_sin_resumen:
            temporal = {
                'paciente': str(entrada.paciente),
                'area': str(entrada.area),
                'terapeuta': str(entrada.empleado),
            }
            info_sin_resumen.append(temporal)

        return JsonResponse(
            {'status': True, 'info_con_resumen': info_con_resumen, 'info_sin_resumen': info_sin_resumen}, safe=False)

@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador']))
def consultar_informe_paciente_ajax(request):
    fecha = request.GET.get('fecha')
    if fecha == '':
        return JsonResponse({'status': False}, safe=False)
    fecha = fecha.split('-')
    month = int(fecha[0])
    year = int(fecha[1])
    dia_final = calendar.monthrange(year, month)[1]
    fecha_inicial = datetime.datetime(year, month, 1)
    fecha_final = datetime.datetime(year, month, dia_final)
    datos = []
    areas = Area.objects.exclude(nombre='Administrativa')
    condiciones = {}
    for area in areas:
        condiciones['resumen_area%s' % area.id] = Count('resumenes',
                                                        filter=Q(resumenes__fecha__range=[fecha_inicial, fecha_final],
                                                                 resumenes__area=area), distinct=True)
        condiciones['entradas_area%s' % area.id] = Count('entradas_paciente',
                                                        filter=Q(entradas_paciente__fecha__range=[fecha_inicial, fecha_final],
                                                                 entradas_paciente__area=area), distinct=True)
    pacientes = Paciente.objects.filter(estado='Activo', entradas_paciente__fecha__range=[fecha_inicial, fecha_final]).annotate(**condiciones).values()
    resumenes = list(Resumen.objects.filter(fecha__range=[fecha_inicial, fecha_final]).prefetch_related('paciente'))
    for paciente in pacientes:
        temp = {'paciente': '%s - %s %s' %(paciente['identificacion'], paciente['nombre'], paciente['apellido'])}
        for area in areas:
            if paciente['resumen_area%s' % area.id]:
                informe = next(filter(lambda x: x.paciente.identificacion == paciente['identificacion'] and x.area == area,  resumenes))
                temp[str(area)] = "Si" + "-" + str(informe.id)
            elif paciente['entradas_area%s' % area.id]:
                temp[str(area)] = "No"
            else:
                temp[str(area)] = "N/A"
        datos.append(temp)

    return JsonResponse({'status': True, 'datos': datos}, safe=False)

@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador', 'Auxiliar administrativo']))
def consultar_informe_paciente_consolidado_ajax(request):
    fecha = request.GET.get('fecha')
    if fecha == '':
        return JsonResponse({'status': False}, safe=False)
    fecha = fecha.split('-')
    month = int(fecha[0])
    year = int(fecha[1])
    dia_final = calendar.monthrange(year, month)[1]
    fecha_inicial = datetime.datetime(year, month, 1)
    fecha_final = datetime.datetime(year, month, dia_final)
    datos = []
    areas = Area.objects.exclude(nombre='Administrativa')
    #ACOMODAR ESTA PARTE DE ENRADAS PACIENTE
    pacientes = Paciente.objects.filter(estado='Activo', resumenes__fecha__range=[fecha_inicial, fecha_final]).distinct()
    for paciente in pacientes:
        temp = {'paciente': str(paciente)}
        for area in areas:
            if paciente.resumenes.filter(fecha__range=[fecha_inicial, fecha_final], area=area).exists():
                informe = Resumen.objects.get(area=area, paciente=paciente, fecha__range=[fecha_inicial, fecha_final])
                if informe.revisado:
                    temp[str(area)] = "Revisado"
                else:
                    temp[str(area)] = "Sin revisar"
            else:
                temp[str(area)] = "N/A"
        datos.append(temp)
    return JsonResponse({'status': True, 'datos': datos}, safe=False)
