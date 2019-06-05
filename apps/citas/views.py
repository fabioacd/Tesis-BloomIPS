from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
import json
from utils.utils import check_cargos
from django.contrib import messages


# Create your views here.
@login_required
@user_passes_test(check_cargos(['Administrador', 'Coordinador']))
def ver_citas(request):
    print('here')
    contexto = {}
    return render(request, 'ver_citas.html', contexto)
