from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .forms import AgregarAreaForm, ModificarAreaForm
from .models import Area

# Create your views here.


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