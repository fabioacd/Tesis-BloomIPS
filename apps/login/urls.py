from django.conf.urls import url
from django.urls import path

from apps.login.views import login_user

urlpatterns = [
    path('', login_user, name='login')
]