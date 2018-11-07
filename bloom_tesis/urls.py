
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
#from django.urls import path,
from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('empleado/', include('apps.empleado.urls')),
    path('paciente/', include('apps.paciente.urls')),
    path('login/', include('apps.login.urls'), name = "login"),
    path('evento_adverso/', include('apps.evento_adverso.urls')),
    path('select2/', include('django_select2.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)