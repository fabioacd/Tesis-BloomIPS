from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .forms import AgregarAreaForm

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
