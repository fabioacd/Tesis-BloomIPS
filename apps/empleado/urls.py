from django.urls import path
from apps.empleado.views import agregar_area, consultar_area, modificar_area
from apps.empleado.views import agregar_eps, consultar_eps, modificar_eps

urlpatterns = [
    path('agregar_area/', agregar_area, name='agregar_area'),
    path('consultar_area/', consultar_area, name='consultar_area'),
    path('modificar_area/<id_area>/', modificar_area, name='modificar_area'),
    path('agregar_eps/', agregar_eps, name='agregar_eps'),
    path('modificar_eps/<nit>/', modificar_eps, name='modificar_eps'),
    path('consultar_eps/', consultar_eps, name='consultar_eps'),
]
