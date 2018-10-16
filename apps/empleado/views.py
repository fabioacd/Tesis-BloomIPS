from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .forms import AgregarAreaForm, ModificarAreaForm, AgregarEpsForm, ModificarEpsForm, AgregarEmpleadoForm, \
    ModificarEmpleadoForm
from .models import Area, Empleado
from apps.paciente.models import Eps

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