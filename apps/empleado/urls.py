from django.urls import path
from apps.empleado.views import agregar_area, consultar_area


urlpatterns = [
    path('agregar_area/', agregar_area, name='agregar_area'),
    path('consultar_area/', consultar_area, name='consultar_area')
]