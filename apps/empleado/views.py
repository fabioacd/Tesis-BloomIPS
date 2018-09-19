from django.http import JsonResponse
import json
from django.shortcuts import render
from django.template.defaultfilters import safe, time

from .forms import AgregarEmpleadoForm, AgregarEpsForm, AgregarAreaForm, ModificarAreaForm, \
    ModificarEmpleadoForm, AgregarResumenForm, ModificarEpsForm, AgregarConsolidadoForm, \
    ModificarResumenForm
from django.contrib import messages
from .models import Area, Resumen, Empleado
from apps.paciente.models import Entrada, Paciente, Eps
from django.shortcuts import redirect


# Create your views here.

def index(request):
    return render(request, 'empleado/templates/resumen/agregar_resumen.html')


def agregar_empleado(request):
    form = AgregarEmpleadoForm()
    if request.method == 'POST':
        form = AgregarEmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = AgregarEmpleadoForm()
            messages.success(request, 'Empleado registrado exitosamente')
        else:
            messages.error(request, 'No se pudo registrar el empleado')
    # elif  not request.user.is_authenticated:
    # return redirect('login')
    contexto = {'form': form}
    return render(request, 'empleado/agregar_empleado.html', contexto)


def consultar_empleado(request):
    empleados = list(Empleado.objects.all())
    contexto = {'empleados': empleados}
    return render(request, 'empleado/consultar_empleado.html', contexto)


def modificar_empleado(request, id_empleado):
    empleado = Empleado.objects.get(username=id_empleado)

    if request.method == 'POST':
        form = ModificarEmpleadoForm(request.POST, request.FILES, instance=empleado)

        if form.is_valid():
            form.save()
            form = ModificarEmpleadoForm(instance=empleado)
            messages.success(request, 'Usuario modificado exitosamente')
            return redirect(consultar_empleado)
        else:
            messages.error(request, 'No se pudo modificar el empleado')

    else:
        form = ModificarEmpleadoForm(instance=empleado)

    contexto = {'form': form, 'empleado': empleado}
    return render(request, 'empleado/modificar_empleado.html', contexto)


# --------------------AREA-----------------------------------------------------
def agregar_area(request):
    form = AgregarAreaForm()
    if request.method == 'POST':
        form = AgregarAreaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Área registrada exitosamente')
            return redirect(agregar_area)
        else:
            print(form.errors)
            messages.error(request, 'No se pudo registrar el área')
    # elif  not request.user.is_authenticated:
    # return redirect('login')
    contexto = {'form': form}
    return render(request, 'area/agregar_area.html', contexto)


def consultar_area(request):
    areas = list(Area.objects.all())
    contexto = {'areas': areas}
    return render(request, 'area/consultar_area.html', contexto)


def modificar_area(request, id_area):
    area = Area.objects.get(id=id_area)

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


# ----------------------RESUMEN--------------------------------------------

def agregar_resumen(request):
    form = AgregarResumenForm()
    if request.method == 'POST':
        form = AgregarResumenForm(request.POST)
        if form.is_valid():
            resumen = form.save(commit=False)
            resumen.area = request.user.area
            resumen.empleado = request.user
            resumen.save()
            form = AgregarResumenForm()
            messages.success(request, 'Resumen registrado exitosamente')
        else:
            messages.error(request, 'No se pudo registrar el resumen')
    contexto = {'form': form}
    return render(request, 'resumen/agregar_resumen.html', contexto)


def consultar_resumen(request):
    resumenes = Resumen.objects.all()
    contexto = {'resumenes': resumenes}
    return render(request, 'resumen/consultar_resumen.html', contexto)

def modificar_resumen(request, id_resumen):
    resumen = Resumen.objects.get(id=id_resumen)
    if resumen.revisado:
        messages.error(request, 'El resumen ya ha sido revisado')
        return redirect('consultar_resumen')
    if request.method == 'POST':
        form = ModificarResumenForm(request.POST, instance=resumen)

        if form.is_valid():
            form.save()
            messages.success(request, 'Resumen modificado exitosamente')
            return redirect(consultar_resumen)
        else:
            messages.error(request, 'No se pudo modificar el resumen')

    else:
        form = ModificarResumenForm(instance=resumen)

    contexto = {'form': form, 'resumen': resumen}
    return render(request, 'resumen/modificar_resumen.html', contexto)


'''
empleado = models.ForeignKey('empleado.Empleado', on_delete=models.CASCADE)  # FORANEA
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)  # FORANEA
    fecha = models.DateField()
    hora = models.TimeField()
    descripcion = models.CharField(max_length=3000)
'''


def get_entradas_ajax(request):
    # --------------------------------------------------------------------------

    fechas = request.GET.get('rango_fecha')
    fecha_inicial = fechas[6] + fechas[7] + fechas[8] + fechas[9] + "-" + fechas[0] + fechas[1] + "-" + fechas[3] + \
                    fechas[4]
    fecha_final = fechas[19] + fechas[20] + fechas[21] + fechas[22] + "-" + fechas[13] + fechas[14] + "-" + fechas[16] + \
                  fechas[17]
    id_paciente = request.GET.get('id_paciente')
    id_empleado = request.GET.get('id_empleado')
    print(
        'Fecha Inicial: ' + fecha_inicial + ' Fecha Final: ' + fecha_final + ' Empleado: ' + id_empleado + ' Paciente: ' + id_paciente)
    paciente = Paciente.objects.get(identificacion=id_paciente)
    empleado = Empleado.objects.get(username=id_empleado)
    print('Si pasa por aca mi socio')
    entradas_paciente = Entrada.objects.filter(paciente=paciente, fecha__range=[fecha_inicial, fecha_final])
    area = empleado.area
    empleados_area = area.empleados_area.all()
    entradas = entradas_paciente.filter(empleado__in=empleados_area)
    print(entradas)
    # --------------------------------------------------------------------------
    datos = []
    for entrada in entradas:
        temporal = {
            'fecha': str(entrada.fecha),
            'hora': str(entrada.hora),
            'descripcion': entrada.descripcion
        }
        datos.append(temporal)
    print(datos)
    datosJson = json.dumps(datos)
    return JsonResponse(datosJson, safe=False)


# --------------------EPS-----------------------------------------------------
def agregar_eps(request):
    form = AgregarEpsForm()
    if request.method == 'POST':
        form = AgregarEpsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Eps registrada exitosamente')
            return redirect(agregar_eps)
        else:
            print(form.errors)
            messages.error(request, 'No se pudo registrar la eps')
    # elif  not request.user.is_authenticated:
    # return redirect('login')
    contexto = {'form': form}
    return render(request, 'eps/agregar_eps.html', contexto)


def modificar_eps(request, nit):
    eps = Eps.objects.get(nit=nit)

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


def consultar_eps(request):
    eps = list(Eps.objects.all())
    contexto = {'eps': eps}
    return render(request, 'eps/consultar_eps.html', contexto)


# --------------------CONSOLIDADO-----------------------------------------------------

def agregar_consolidado(request):
    form = AgregarConsolidadoForm()
    if request.method == 'POST':
        form = AgregarConsolidadoForm(request.POST)
        if form.is_valid():
            consolidado = form.save(commit=False)
            resumenes = consolidado.paciente.resumenes.filter(fecha__range = [consolidado.fecha_inicio, consolidado.fecha_fin])
            if(resumenes.count() > 0):
                consolidado.save()
            else:
                messages.error(request, 'No hay resúmenes en el rango de fechas dado')
                return redirect('agregar_consolidado')
            for resumen in resumenes:
                resumen.revisado = True
                resumen.save()
                consolidado.resumenes.add(resumen)

            messages.success(request, 'Consolidado registrado exitosamente')
        else:
            print(form.errors)
            messages.error(request, 'No se pudo registrar el consolidado')
    contexto = {'form': form}
    return render(request, 'consolidado/agregar_consolidado.html', contexto)


def get_consolidado_ajax(request):
    datos = []
    try:
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        id_paciente = int(request.GET.get('id_paciente'))
        paciente = Paciente.objects.get(identificacion=id_paciente)
        resumenes_paciente = paciente.resumenes.filter(fecha__range = [fecha_inicio, fecha_fin], revisado = False).order_by('area', 'id')

        for resumen in resumenes_paciente:
            temporal = {
                'area': str(resumen.area),
                'descripcion': str(resumen.descripcion)
            }
            datos.append(temporal)

        print(datos)
        datosJson = json.dumps(datos)
        return JsonResponse(datosJson, safe=False)
    except Exception:
        # En caso de que se lance la excepción, llega vacío el json al js y con la evaluación que hay pone en el campo "El paciente no tiene resúmenes"
        print(datos)
        datosJson = json.dumps(datos)
        return JsonResponse(datosJson, safe=False)

def generar_consolidados(request):
    '''fecha = request.GET.get('fecha')
    pacientes = Paciente.objects.all()
    print(pacientes)
    resumenes_paciente = pacientes.resumenes.filter(fecha=[fecha], revisado=False).order_by('area', 'id')'''
    return render(request, 'consolidado/generar_consolidados.html')


# --------------------CONSOLIDADO-----------------------------------------------------
