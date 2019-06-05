from django.urls import path
from apps.paciente.views import registrar_paciente, consultar_paciente, ver_paciente, modificar_paciente, \
    agregar_evolucion_diaria, consultar_evolucion_diaria, get_evo_diaria_ajax, modificar_evolucion_diaria, \
    get_pacientes_entradas_ajax, get_entradas_dia_ajax, carga_masiva_cie10, agregar_archivo_paciente, \
    eliminar_archivo_paciente_ajax, get_diagnosticos_ajax, ajax_filtro_consultar_paciente

urlpatterns = [
    path('registrar_paciente/', registrar_paciente, name='registrar_paciente'),
    path('consultar_paciente/', consultar_paciente, name='consultar_paciente'),
    path('ver_paciente/<id_paciente>/', ver_paciente, name='ver_paciente'),
    path('modificar_paciente/<id_paciente>/', modificar_paciente, name='modificar_paciente'),
    path('agregar_evolucion_diaria/', agregar_evolucion_diaria, name='agregar_evolucion_diaria'),
    path('consultar_evolucion_diaria/', consultar_evolucion_diaria, name='consultar_evolucion_diaria'),
    path('ajax_evo_diaria/', get_evo_diaria_ajax, name='get_evo_diaria_ajax'),
    path('get_pacientes_ent_ajax/', get_pacientes_entradas_ajax, name='get_pacientes_entradas_ajax'),
    path('get_entradas_dia_ajax/', get_entradas_dia_ajax, name='get_entradas_dia_ajax'),
    path('modificar_evolucion_diaria/<id_entrada>/', modificar_evolucion_diaria, name='modificar_evolucion_diaria'),
    path('carga_cie10/', carga_masiva_cie10, name='carga_cie10'),
    path('agregar_archivo_paciente/', agregar_archivo_paciente, name='agregar_archivo_paciente'),
    path('eliminar_archivo_paciente_ajax', eliminar_archivo_paciente_ajax, name='eliminar_archivo_paciente_ajax'),
    path('get_diagnosticos_ajax', get_diagnosticos_ajax, name='get_diagnosticos_ajax'),
    path('ajax_filtro_consultar_paciente/', ajax_filtro_consultar_paciente.as_view(), name='ajax_filtro_consultar_paciente'),
]
