from django import forms
from .models import Post, Categoria
from apps.comentario.models import Comentario 


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']



class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'subtitulo', 'texto', 'categoria', 'imagen', 'activo']

class NuevaCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
