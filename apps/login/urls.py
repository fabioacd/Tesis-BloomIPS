from django.conf.urls import url
from django.urls import path

from apps.login.views import login_user, bloqueo_user
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', login_user, name='login'),
    path('bloqueo', bloqueo_user, name='bloqueo')
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)