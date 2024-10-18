from .forms import RegistroUsuarioForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import Group

# Create your views here.


class RegistrarUsuario(CreateView):
    template_name = 'registration/registrar.html'
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('apps.usuario:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Usuario registrado correctamente. Por favor, inicie sesión con sus nuevas credenciales.')
        group = Group.objects.get(name='Registrado')
        self.object.groups.add(group)
        return response

class LoginUsuario(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        messages.success(self.request, 'Login exitoso')

        return self.request.GET.get('next', reverse('index'))
    
class LogoutUsuario(LogoutView):
    template_name = 'registration/logout.html'

    def get_success_url(self):
        messages.success(self.request, 'Logout exitoso')

        return reverse('apps.usuario:login')
