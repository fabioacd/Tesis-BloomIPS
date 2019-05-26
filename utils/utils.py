import os
import base64
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
import datetime, calendar
from io import BytesIO
from xhtml2pdf import pisa

from bloomips.settings import MEDIA_URL, MEDIA_ROOT, BASE_DIR


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = os.path.join(BASE_DIR, 'static')    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/
    # convert URIs to absolute system paths
    if "png" in uri:
        path = os.path.join(mRoot, uri.replace(sUrl, ""))
        path = path.replace("\\", "/")
    else:
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
        path = path.replace("\\", "/")
    # else:
        # return uri  # handle absolute uri (ie: http://some.tld/foo.png)
    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path


# Funcion que renderiza un html a pdf
def convertir_a_pdf(template_src, nombre_archivo, contexto={}):
    template = get_template(template_src)
    html = template.render(contexto)
    response = HttpResponse(content_type='application/pdf')
    nombre_archivo += ".pdf"
    content = 'attachment; filename="nombre"'
    content = content.replace('nombre', nombre_archivo)
    response['Content-Disposition'] = content
    pisaStatus = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
        return HttpResponse('Error al generar el PDF')
    return response


def rango_fechas_informe_mensual():
    fecha_actual = datetime.datetime.now().date()
    dia_final = calendar.monthrange(fecha_actual.year, fecha_actual.month)[1]
    fecha_inicial = datetime.datetime(fecha_actual.year, fecha_actual.month, 1)
    fecha_final = datetime.datetime(fecha_actual.year, fecha_actual.month, dia_final)

    return [fecha_inicial, fecha_final]


def check_cargos(cargos):
    def check(user):
        if user.cargo in cargos:
            return True
        else:
            raise PermissionDenied
    return check


def nombre_mes(mes):
    switch = {
        'January': 'Enero',
        'February': 'Febrero',
        'March': 'Marzo',
        'April': 'Abril',
        'May': 'Mayo',
        'June': 'Junio',
        'July': 'Julio',
        'August': 'Agosto',
        'September': 'Septiembre',
        'October': 'Octubre',
        'November': 'Noviembre',
        'December': 'Diciembre',
    }
    return switch.get(mes)


def directorio_archivos_empleado(instance, filename):
    return "empleado/%s_%s/%s" % (instance.username, instance.first_name, filename.encode('ascii', 'ignore').decode('ascii'))


def directorio_archivos_paciente(instance, filename):
    return "paciente/%s_%s/%s" % (instance.identificacion, instance.nombre, filename.encode('ascii', 'ignore').decode('ascii'))


def directorio_archivos_extra_paciente(instance, filename):
    return "paciente/%s_%s/%s" % (instance.paciente.identificacion, instance.paciente.nombre, filename.encode('ascii', 'ignore').decode('ascii'))