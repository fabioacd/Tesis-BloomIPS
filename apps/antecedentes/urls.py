from django.urls import path
from apps.antecedentes.views import registrar_antecedentes_personales, registrar_antecedentes_psicosociales, \
                                    registrar_antecedentes_gestacionales, registrar_antecedentes_familiares, \
                                    consultar_antecedentes_personales, get_antecedente_personal_ajax, \
                                    consultar_antecedentes_gestacionales, get_antecedente_gestacional_ajax, \
                                    consultar_antecedentes_familiares, get_antecedente_familiar_ajax, \
                                    consultar_antecedentes_psicosociales, get_antecedentes_psicosocial_ajax, \
                                    modificar_antecedentes_gestacionales, modificar_antecedentes_familiares, \
                                    modificar_antecedentes_personales, modificar_antecedentes_psicosociales

urlpatterns = [
    path('registrar_antecedentes_personales/', registrar_antecedentes_personales,
         name='registrar_antecedentes_personales'),
    path('registrar_antecedentes_psicosociales/', registrar_antecedentes_psicosociales,
         name='registrar_antecedentes_psicosociales'),
    path('registrar_antecedentes_gestacionales/', registrar_antecedentes_gestacionales,
         name='registrar_antecedentes_gestacionales'),
    path('registrar_antecedentes_familiares/', registrar_antecedentes_familiares,
         name='registrar_antecedentes_familiares'),
    path('consultar_antecedentes_personales/', consultar_antecedentes_personales,
         name='consultar_antecedentes_personales'),
    path('consultar_antecedentes_gestacionales/', consultar_antecedentes_gestacionales,
         name='consultar_antecedentes_gestacionales'),
    path('consultar_antecedentes_familiares/', consultar_antecedentes_familiares,
         name='consultar_antecedentes_familiares'),
    path('consultar_antecedentes_psicosociales/', consultar_antecedentes_psicosociales,
         name='consultar_antecedentes_psicosociales'),
    path('modificar_antecedentes_gestacionales/', modificar_antecedentes_gestacionales,
         name='modificar_antecedentes_gestacionales'),
    path('modificar_antecedentes_familiares/', modificar_antecedentes_familiares,
         name='modificar_antecedentes_familiares'),
    path('modificar_antecedentes_personales/', modificar_antecedentes_personales,
         name='modificar_antecedentes_personales'),
    path('modificar_antecedentes_psicosociales/', modificar_antecedentes_psicosociales,
         name='modificar_antecedentes_psicosociales'),
    path('ajax_personal/', get_antecedente_personal_ajax, name='get_antecedente_personal_ajax'),
    path('ajax_gestacional/', get_antecedente_gestacional_ajax, name='get_antecedente_gestacional_ajax'),
    path('ajax_familiar/', get_antecedente_familiar_ajax, name='get_antecedente_familiar_ajax'),
    path('ajax_psicosocial/', get_antecedentes_psicosocial_ajax, name='get_antecedentes_psicosocial_ajax')
]
