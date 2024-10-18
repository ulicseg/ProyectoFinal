from .forms import RegistroUsuarioForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import Group
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
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
    
class LogoutUsuario(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logout exitoso')
        return redirect(reverse('apps.usuario:login'))

    def get_success_url(self):
        messages.success(self.request, 'Logout exitoso')

        return reverse('apps.usuario:login')
    
class UsuarioListView(LoginRequiredMixin,ListView):
    model = User
    template_name = 'usuario/usuario_list.html'
    context_object_name = 'usuarios'


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(is_superuser=True)
        return queryset
    
class UsuarioDetailView(LoginRequiredMixin,ListView):
    model = User
    template_name = 'usuario/usuario_detail.html'
    context_object_name = 'usuario'


class UsuarioDeleteView(LoginRequiredMixin,DeleteView):
    model = User
    template_name = 'usuario/eliminar_usuario.html'
    context_object_name = 'usuario'
    success_url = reverse_lazy('apps.usuario:usuario_list')
    