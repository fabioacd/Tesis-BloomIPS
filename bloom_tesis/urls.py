
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
#from django.urls import path,
from django.conf.urls import url, include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('empleado/', include('apps.empleado.urls')),
    path('login/', include('apps.login.urls'), name = "login"),
]
