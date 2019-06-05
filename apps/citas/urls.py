from django.urls import path
from apps.citas.views import ver_citas

urlpatterns = [
    path('hola', ver_citas, name='ver_citas'),
]
