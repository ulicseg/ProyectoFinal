from .models import Post, Categoria
from .forms import ComentarioForm, CreatePostForm, NuevaCategoriaForm
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from apps.comentario.models import Comentario 
from django.http import Http404
from django.contrib.auth.models import Group

# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = "posts/posts.html" 
    context_object_name = "posts" 

    def get_queryset(self):
        queryset = super().get_queryset()
        orden = self.request.GET.get('orden')
        if orden == 'reciente':
            queryset = queryset.order_by('-fecha')
        elif orden == 'antiguo':
            queryset = queryset.order_by('fecha')
        elif orden == 'alfabetico':
            queryset = queryset.order_by('titulo')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden'] = self.request.GET.get('orden', 'reciente')
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/posts_individual.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        context['comentarios'] = Comentario.objects.filter(post=self.object)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.post_id = self.kwargs['id']
            comentario.save()
            return redirect('apps.posts:post_individual', id=self.object.id)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/agregarComentario.html'
    success_url = 'comentario/comentarios/'
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.post_id = self.kwargs['id']
        return super().form_valid(form)

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'posts/crear_post.html'
    success_url = reverse_lazy('apps.posts:posts')

class CategoriaCreateView(LoginRequiredMixin,CreateView):
    model = Categoria
    form_class = NuevaCategoriaForm
    template_name = 'posts/crear_categoria.html'
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('apps.posts:crear_post')

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'posts/categoria_list.html'
    context_object_name = 'categorias'

class CategoriaDeleteView(LoginRequiredMixin,DeleteView):
    model = Categoria
    template_name = 'posts/categoria_confirm_delete.html'
    success_url = reverse_lazy('apps.posts:categoria_list')

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'posts/modificar_post.html'
    success_url = reverse_lazy('apps.posts:posts')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['imagen'].required = False
        return form

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/eliminar_post.html'
    success_url = reverse_lazy('apps.posts:posts')

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Colaborador').exists() or post.autor == self.request.user

    def handle_no_permission(self):
        return render(self.request, self.template_name, {
            'unauthorized': True
        })

class PostPorCategoriaView(ListView):
    model = Post
    template_name = 'posts/posts_por_categoria.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(categoria=self.kwargs['pk'])
