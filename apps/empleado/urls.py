from django.urls import path
from apps.empleado.views import agregar_area


urlpatterns = [
    path('agregar_area/', agregar_area, name='agregar_area'),
]