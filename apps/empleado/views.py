import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .forms import AgregarAreaForm, ModificarAreaForm, AgregarEpsForm, ModificarEpsForm, AgregarEmpleadoForm, \
    ModificarEmpleadoForm, ModificarResumenForm, AgregarResumenForm
from .models import Area, Empleado, Resumen
from apps.paciente.models import Eps, Paciente, Entrada


# Create your views here.

@login_required
def index(request):
    return render(request, 'empleado/index.html')

# --------------------AREA-----------------------------------------------------
@login_required
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

@login_required
def consultar_area(request):
    areas = list(Area.objects.all())
    contexto = {'areas': areas}
    return render(request, 'area/consultar_area.html', contexto)

@login_required
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

# -------------------------------EPS--------------------------------------------
def administrador_check(user):
    return user.check_cargo('Administrador')

@login_required
@user_passes_test(administrador_check, login_url='index')
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

@login_required
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

@login_required
def consultar_eps(request):
    eps = list(Eps.objects.all())
    contexto = {'eps': eps}
    return render(request, 'eps/consultar_eps.html', contexto)

#---------------------EMPLEADO-----------------------------------------------------


@login_required
def agregar_empleado(request):
    form = AgregarEmpleadoForm()
    if request.method == 'POST':
        form = AgregarEmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            empleado = Empleado.objects.get(username=form.username)
            form = AgregarEmpleadoForm()
            messages.success(request, 'Empleado registrado exitosamente')
        else:
            messages.error(request, 'No se pudo registrar el empleado')
    # elif  not request.user.is_authenticated:
    # return redirect('login')
    contexto = {'form': form}
    return render(request, 'empleado/agregar_empleado.html', contexto)

@login_required
def consultar_empleado(request):
    empleados = list(Empleado.objects.all())
    contexto = {'empleados': empleados}
    return render(request, 'empleado/consultar_empleado.html', contexto)

@login_required
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



# ----------------------RESUMEN--------------------------------------------
@login_required
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

@login_required
def consultar_resumen(request):
    resumenes = Resumen.objects.all()
    contexto = {'resumenes': resumenes}
    return render(request, 'resumen/consultar_resumen.html', contexto)

@login_required
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

@login_required
def get_entradas_ajax(request):
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
    # --------------------------------------------------------------------------