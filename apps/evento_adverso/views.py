from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
import json
from apps.empleado.models import Empleado
from apps.evento_adverso.models import SeguimientoEvento
from utils.utils import check_cargos
from .forms import AgregarImplicadoEventoForm, AgregarEventoAdversoForm, ModificarEventoAdversoForm, \
    AgregarSeguimientoForm, RegistrarProtocoloForm, VisualizarProtocoloForm, ModificarImplicadoEventoAdversoForm, \
    ModificarProtocoloForm
from .models import EventoAdverso, ProtocoloLondres, ImplicadoEvento
from django.contrib import messages
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.urls import reverse_lazy
from django.db.models import Q


# Create your views here.
@login_required
def agregar_evento_adverso(request):
    form_evento_adverso = AgregarEventoAdversoForm()
    if request.method == 'POST':
        form_evento_adverso = AgregarEventoAdversoForm(request.POST)
        if form_evento_adverso.is_valid():
            form_evento_adverso.save()
            messages.success(request, 'se agregó el evento adverso')
            return redirect('consultar_evento')
        else:
            messages.error(request, 'Error al registrar el evento adverso, intente nuevamente')

    contexto = {'form_evento_adverso': form_evento_adverso}
    return render(request, 'evento_adverso/agregar_evento_adverso.html', contexto)


@login_required
def agregar_implicado_evento_adverso(request):
    form_crear_implicado = AgregarImplicadoEventoForm()
    if request.method == 'POST':
        form_crear_implicado = AgregarImplicadoEventoForm(request.POST)  # , instance=instancia)
        if form_crear_implicado.is_valid():
            form_crear_implicado.save()
            messages.success(request, 'se agregó el implicado al  evento adverso')
            return redirect(agregar_evento_adverso)
        else:
            messages.error(request, 'Error al registrar el implicado, intente nuevamente')

    contexto = {'form_crear_implicado': form_crear_implicado}
    return render(request, 'implicado/agregar_implicado_evento_adverso.html', contexto)


@login_required
def modificar_implicado_evento_adverso(request, id_implicado):
    implicado = get_object_or_404(ImplicadoEvento, id_implicado=id_implicado)

    if request.method == 'POST':
        form = ModificarImplicadoEventoAdversoForm(request.POST, instance=implicado)

        if form.is_valid():
            form.save()
            messages.success(request, 'Implicado modificado exitosamente')
            return redirect(consultar_implicados_evento_adverso)
        else:
            messages.error(request, 'No se pudo modificar el implicado')

    else:
        form = ModificarImplicadoEventoAdversoForm(instance=implicado)

    contexto = {'form': form, 'implicado': implicado}
    return render(request, 'implicado/modificar_implicado_evento_adverso.html', contexto)


@login_required
def consultar_implicados_evento_adverso(request):
    implicados = list(ImplicadoEvento.objects.all())
    contexto = {'implicados': implicados}
    return render(request, 'implicado/consultar_implicado_evento_adverso.html', contexto)


class ajax_filtro_consultar_implicado(BaseDatatableView):
    # The model we're going to show
    model = ImplicadoEvento

    # define the columns that will be returned
    columns = ['id_implicado', 'seguridad_social', 'nombre', 'modificar']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['id_implicado', 'seguridad_social', 'nombre', '']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 100

    def render_column(self, row, column):
        implicado = row
        if column == 'modificar':
            return reverse_lazy('modificar_implicado_evento_adverso', args=[implicado.id_implicado])
        return super(ajax_filtro_consultar_implicado, self).render_column(row, column)

    def get_initial_queryset(self):
        return ImplicadoEvento.objects.all()

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
                        q |= Q(**{'{0}__icontains'.format(column_name): search})
            qs = qs.filter(q)
        return qs


@login_required
def consultar_evento(request):
    eventos = list(EventoAdverso.objects.all())
    contexto = {'eventos': eventos, 'user': request.user}
    return render(request, 'evento_adverso/consultar_evento_adverso.html', contexto)


class ajax_filtro_consultar_evento(BaseDatatableView):
    model = EventoAdverso
    columns = ['implicado', 'tipos_evento', 'fecha_ocurrencia', 'lugar', 'descripcion', 'modificar']
    order_columns = ['implicado', 'tipos_evento', 'fecha_ocurrencia', 'lugar', 'descripcion', '']
    max_display_length = 100

    def render_column(self, row, column):
        evento = row
        cargo_usuario = self.request.user.cargo
        opciones = []
        if column == 'modificar':

            # Validación botón 'Modificar'
            if cargo_usuario == "Coordinador" or cargo_usuario == "Administrador":
                opciones.append({
                    'texto_boton': 'Modificar',
                    'url': reverse_lazy('modificar_evento', args=[evento.id]),
                    'color': 'btn-primary'
                })
            # Validación botón 'Protocolo Londres'
            if hasattr(evento, 'protocolo_londres') and evento.protocolo_londres is not None and evento.protocolo_londres:
                if cargo_usuario == "Coordinador" or cargo_usuario == "Administrador":
                    opciones.append({
                        'texto_boton': 'Protocolo',
                        'url': reverse_lazy('modificar_protocolo', args=[evento.id]),
                        'color': 'bg-olive'
                    })
                else:
                    opciones.append({
                        'texto_boton': 'Protocolo',
                        'url': reverse_lazy('visualizar_protocolo', args=[evento.id]),
                        'color': 'bg-olive'
                    })
            else:
                opciones.append({
                    'texto_boton': 'Protocolo',
                    'url': reverse_lazy('registrar_protocolo', args=[evento.id]),
                    'color': 'bg-olive'
                })
            # Siempre está presente el botón 'Agregar seguimiento'
            opciones.append({
                'texto_boton': 'Seguimiento',
                'url': reverse_lazy('agregar_seguimiento', args=[evento.id]),
                'color': 'bg-olive'
            })
            return opciones

        if column == 'tipos_evento':
            for tipo_evento in evento.tipos_evento.all():
                if tipo_evento.nombre == 'Otro':
                    opciones.append(evento.otro_tipo_evento)
                else:
                    opciones.append(tipo_evento.nombre)
            return opciones

        return super(ajax_filtro_consultar_evento, self).render_column(row, column)

    def get_initial_queryset(self):
        return EventoAdverso.objects.all()

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
                        if column_name == 'implicado':
                            column_name = 'implicado__nombre'
                        if column_name == 'empleado':
                            realizar_busqueda_base = False
                            q |= Q(**{'{0}__icontains'.format('empleado__first_name'): search}) | Q(
                                **{'{0}__icontains'.format('empleado__last_name'): search}) | Q(
                                **{'{0}__icontains'.format('empleado__username'): search})
                        if column_name == 'tipos_evento':
                            realizar_busqueda_base = False
                            q |= Q(**{'{0}__icontains'.format('tipos_evento__nombre'): search}) | Q(
                                **{'{0}__icontains'.format('otro_tipo_evento'): search})
                        if realizar_busqueda_base:
                            q |= Q(**{'{0}__icontains'.format(column_name): search})
                    if col['search.value']:
                        if column_name == "fecha_ocurrencia":
                            fecha_ocurrencia_filtrada = col['search.value'].lower()
                            qs = qs.filter(fecha_ocurrencia__icontains=fecha_ocurrencia_filtrada)
            qs = qs.filter(q).distinct()
        return qs

@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador']))
def modificar_evento(request, id_evento):
    evento = get_object_or_404(EventoAdverso, id=id_evento)
    if request.method == 'POST':
        form = ModificarEventoAdversoForm(request.POST, instance=evento)

        if form.is_valid():
            form.save()
            messages.success(request, 'Evento modificado exitosamente')
            return redirect(consultar_evento)
        else:
            messages.error(request, 'No se pudo modificar el evento')

    else:
        form = ModificarEventoAdversoForm(instance=evento)

    contexto = {'form': form, 'evento': evento}
    return render(request, 'evento_adverso/modificar_evento_adverso.html', contexto)


@login_required
def agregar_seguimiento(request, id_evento):
    evento = get_object_or_404(EventoAdverso, id=id_evento)

    if request.method == 'POST':
        form = AgregarSeguimientoForm(request.POST)

        if form.is_valid():
            seguimiento = form.save(commit=False)
            seguimiento.evento_adverso = evento
            seguimiento.save()
            form = AgregarSeguimientoForm()
            messages.success(request, 'Seguimiento agregado exitosamente')
        else:
            messages.error(request, 'No se pudo agregar el seguimiento')

    else:
        form = AgregarSeguimientoForm()

    contexto = {'form': form, 'evento': evento}
    return render(request, 'evento_adverso/agregar_seguimiento_evento.html', contexto)


@login_required
def registrar_protocolo(request, id_evento):
    evento = get_object_or_404(EventoAdverso, id=id_evento)

    if request.method == 'POST':
        form = RegistrarProtocoloForm(request.POST, evento=evento)

        if form.is_valid():
            protocolo = form.save(commit=False)
            protocolo.evento_adverso = evento
            protocolo.save()
            messages.success(request, 'Protocolo registrado exitosamente')
            return redirect(consultar_evento)
        else:
            messages.error(request, 'No se pudo registrar el protocolo')

    else:
        form = RegistrarProtocoloForm(evento=evento)

    contexto = {'form_protocolo': form, 'evento': evento}
    return render(request, 'evento_adverso/registrar_protocolo_londres.html', contexto)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador']))
def modificar_protocolo(request, id_evento):
    evento = get_object_or_404(EventoAdverso, id=id_evento)
    protocolo = get_object_or_404(ProtocoloLondres, evento_adverso=id_evento)

    if request.method == 'POST':
        form = ModificarProtocoloForm(request.POST, evento=evento)

        if form.is_valid():
            protocolo = form.save(commit=False)
            protocolo.evento_adverso = evento
            protocolo.save()
            messages.success(request, 'Protocolo modificado exitosamente')
            return redirect(consultar_evento)
        else:
            messages.error(request, 'No se pudo registrar el protocolo')

    else:
        form = ModificarProtocoloForm(instance=protocolo, evento=evento)

    contexto = {'form_protocolo': form, 'evento': evento}
    return render(request, 'evento_adverso/modificar_protocolo_londres.html', contexto)


@login_required
def visualizar_protocolo(request, id_evento):
    protocolo = get_object_or_404(ProtocoloLondres, evento_adverso=id_evento)
    evento = get_object_or_404(EventoAdverso, id=id_evento)

    if request.method == 'POST':
        form = VisualizarProtocoloForm(request.POST, evento=evento)

        if form.is_valid():
            protocolo = form.save(commit=False)
            protocolo.evento_adverso = evento
            protocolo.save()
            return redirect(consultar_evento)
        else:
            messages.error(request, 'No se pudo visualizar el protocolo')

    else:
        form = VisualizarProtocoloForm(instance=protocolo, evento=evento)

    contexto = {'form_protocolo': form, 'evento': evento}
    return render(request, 'evento_adverso/protocolo/visualizar_protocolo_londres.html', contexto)


@login_required
def get_seguimientos_ajax(request):
    # --------------------------------------------------------------------------
    id_evento = request.GET.get('id_evento')
    evento = get_object_or_404(EventoAdverso, id=id_evento)

    try:
        seguimientos = SeguimientoEvento.objects.filter(evento_adverso=evento)
    except SeguimientoEvento.DoesNotExist:
        raise Http404

    # --------------------------------------------------------------------------
    datos = []
    for seguimiento in seguimientos:
        temporal = {
            'fecha': str(seguimiento.fecha),
            'descripcion': str(seguimiento.descripcion),
        }
        datos.append(temporal)
    datosJson = json.dumps(datos)
    return JsonResponse(datosJson, safe=False)


@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador']))
def registrar_seguimiento_ajax(request):
    id_evento = request.POST['id_evento']
    evento = get_object_or_404(EventoAdverso, id=id_evento)

    if request.method == 'POST':
        form = AgregarSeguimientoForm(request.POST)

        if form.is_valid():
            seguimiento = form.save(commit=False)
            seguimiento.evento_adverso = evento
            seguimiento.save()

    else:
        form = AgregarSeguimientoForm()
