from .models import Usuario
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, login


class RegistroUsuarioForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'imagen']


class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def login_usuario(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
    
