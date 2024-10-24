from .forms import RegistroUsuarioForm, CambiarRolForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import Group
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from apps.posts.models import Post
from apps.comentario.models import Comentario
from .models import Usuario

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
    
class UsuarioListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Usuario
    template_name = 'usuario/usuario_list.html'
    context_object_name = 'usuarios'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name__in=['Administrador', 'Colaborador']).exists()

    def handle_no_permission(self):
        return render(self.request, self.template_name, {
            'unauthorized': True
        })

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(is_superuser=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authorized'] = self.test_func()
        return context
    
class UsuarioDetailView(LoginRequiredMixin,ListView):
    model = Usuario
    template_name = 'usuario/usuario_detail.html'
    context_object_name = 'usuario'


class UsuarioDeleteView(LoginRequiredMixin,DeleteView):
    model = Usuario
    template_name = 'usuario/eliminar_usuario.html'
    context_object_name = 'usuario'
    success_url = reverse_lazy('apps.usuario:usuario_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        colaborador_group= Group.objects.get(name='Colaborador')
        es_colaborador = colaborador_group in self.object.groups.all()
        context['es_colaborador'] = es_colaborador
        return super().get_context_data(**kwargs)
    
    def post(self, request, *args, **kwargs):
        eliminar_comentarios = request.POST.get('eliminar_comentarios', False)
        eliminar_posts = request.POST.get('eliminar_posts', False)
        self.object = self.get_object()
        if eliminar_comentarios:
            Comentario.objects.filter(usuario=self.object).delete()

        if eliminar_posts:
            Post.objects.filter(usuario=self.object).delete()
        messages.success(request, f'Usuario {self.object.username} eliminado correctamente')
        return super().post(request, *args, **kwargs)

class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'usuario/usuario_update.html'
    fields = ['username', 'email', 'first_name', 'last_name']
    success_url = reverse_lazy('apps.usuario:usuario_list')

    def form_valid(self, form):
        messages.success(self.request, f'Usuario {form.instance.username} actualizado correctamente')
        return super().form_valid(form)

class EditarPerfilView(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'usuario/editar_perfil.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'imagen']  # Añadí 'imagen' aquí
    success_url = reverse_lazy('index')  # Cambiado a 'index' o la página que prefieras

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)

# Agregar nueva vista para cambiar rol
class CambiarRolView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name__in=['Administrador', 'Colaborador']).exists()

    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        form = CambiarRolForm(request.POST)
        if form.is_valid():
            nuevo_rol = form.cleaned_data['rol']
            usuario.groups.clear()
            grupo = Group.objects.get(name=nuevo_rol)
            usuario.groups.add(grupo)
            messages.success(request, f'Rol de {usuario.username} cambiado a {nuevo_rol}')
        return redirect('apps.usuario:usuario_list')
