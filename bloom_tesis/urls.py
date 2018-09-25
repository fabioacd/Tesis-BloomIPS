
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
    path('login/', include('apps.login.urls'), name = "login"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)