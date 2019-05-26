from apps.empleado.models import Empleado
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label=False,)
    password = forms.CharField(required=True, label=False, widget = forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Identificacion"
        self.fields['password'].widget.attrs['placeholder'] = "Contraseña"
