from django.contrib import admin
from .models import Post, Categoria


# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'subtitulo', 'fecha', 'activo', 'categoria')


admin.site.register(Categoria)

