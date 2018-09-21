from django.urls import path
from apps.empleado.views import agregar_area, consultar_area, modificar_area


urlpatterns = [
    path('agregar_area/', agregar_area, name='agregar_area'),
    path('consultar_area/', consultar_area, name='consultar_area'),
    path('modificar_area/<id_area>/', modificar_area, name='modificar_area')
]