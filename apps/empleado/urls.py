from django.urls import path
from apps.empleado.views import informacion_personal, consultar_resumen, agregar_eps, consultar_eps, modificar_eps, \
    generar_consolidado, get_pacientes_informe_ajax, dashboard, ajax_filtro_consultar_area, ajax_filtro_consultar_eps, \
    ajax_filtro_consultar_resumen
from apps.empleado.views import agregar_area, modificar_area, consultar_area
from apps.empleado.views import agregar_empleado, consultar_empleado, modificar_empleado
from apps.empleado.views import agregar_resumen, get_entradas_ajax, modificar_resumen, ver_resumen, consultar_informe_area, consultar_informe_area_ajax, consultar_informe_paciente, consultar_informe_paciente_ajax, agregar_resumen_especifico
from apps.empleado.views import agregar_consolidado, generar_pdf_informe_mensual, consultar_informe_paciente_consolidado_ajax, ajax_filtro_consultar_empleado

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('informacion_personal', informacion_personal, name='informacion_personal'),
    path('agregar_empleado/', agregar_empleado, name='agregar_empleado'),
    path('consultar_empleado/', consultar_empleado, name='consultar_empleado'),
    path('modificar_empleado/<id_empleado>/', modificar_empleado, name='modificar_empleado'),
    path('modificar_area/<id_area>/', modificar_area, name='modificar_area'),
    path('agregar_area/', agregar_area, name='agregar_area'),
    path('consultar_area/', consultar_area, name='consultar_area'),
    path('ajax_filtro_consultar_area/', ajax_filtro_consultar_area.as_view(), name='ajax_filtro_consultar_area'),
    path('agregar_resumen/', agregar_resumen, name='agregar_resumen'),
    path('agregar_resumen_especifico/<id_paciente>/<nombre_area>/<id_terapeuta>/<fecha>', agregar_resumen_especifico, name='agregar_resumen_especifico'),
    path('consultar_resumen/', consultar_resumen, name='consultar_resumen'),
    path('ajax_filtro_consultar_resumen/', ajax_filtro_consultar_resumen.as_view(), name='ajax_filtro_consultar_resumen'),
    path('consultar_informe_area/', consultar_informe_area, name='consultar_informe_area'),
    path('consultar_informe_area_ajax/', consultar_informe_area_ajax, name='consultar_informe_area_ajax'),
    path('consultar_informe_paciente/', consultar_informe_paciente, name='consultar_informe_paciente'),
    path('consultar_informe_paciente_ajax/', consultar_informe_paciente_ajax, name='consultar_informe_paciente_ajax'),
    path('modificar_resumen/<id_resumen>', modificar_resumen, name='modificar_resumen'),
    path('ver_resumen/<id_resumen>', ver_resumen, name='ver_resumen'),
    path('agregar_eps/', agregar_eps, name='agregar_eps'),
    path('modificar_eps/<nit>/', modificar_eps, name='modificar_eps'),
    path('ajax_filtro_consultar_eps/', ajax_filtro_consultar_eps.as_view(), name='ajax_filtro_consultar_eps'),
    path('consultar_eps/', consultar_eps, name='consultar_eps'),
    path('agregar_consolidado/', agregar_consolidado, name='agregar_consolidado'),
    path('consultar_informe_paciente_consolidado_ajax/', consultar_informe_paciente_consolidado_ajax, name='consultar_informe_paciente_consolidado_ajax'),
    path('ajax/', get_entradas_ajax, name='get_entradas_ajax'),
    path('get_pacientes_ajax/', get_pacientes_informe_ajax, name='get_pacientes_informe_ajax'),
    path('generar_consolidado/<id_paciente>/<fecha>/<tipo_area>', generar_consolidado, name='generar_consolidado'),
    path('generar_pdf_informe_mensual/<id_resumen>', generar_pdf_informe_mensual, name='generar_pdf_informe_mensual'),
    path('ajax_filtro_consultar_empleado/', ajax_filtro_consultar_empleado.as_view(), name='ajax_filtro_consultar_empleado'),
]
