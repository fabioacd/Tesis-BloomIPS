from django.urls import path
from apps.empleado.views import agregar_area, consultar_area, modificar_area, agregar_empleado, consultar_empleado, \
    modificar_empleado, index
from apps.empleado.views import agregar_eps, consultar_eps, modificar_eps

urlpatterns = [
    path('', index, name='index'),
    path('agregar_area/', agregar_area, name='agregar_area'),
    path('consultar_area/', consultar_area, name='consultar_area'),
    path('modificar_area/<id_area>/', modificar_area, name='modificar_area'),
    path('agregar_eps/', agregar_eps, name='agregar_eps'),
    path('modificar_eps/<nit>/', modificar_eps, name='modificar_eps'),
    path('consultar_eps/', consultar_eps, name='consultar_eps'),
    path('agregar_empleado/', agregar_empleado, name='agregar_empleado'),
    path('consultar_empleado/', consultar_empleado, name='consultar_empleado'),
    path('modificar_empleado/<id_empleado>/', modificar_empleado, name='modificar_empleado'),
]
