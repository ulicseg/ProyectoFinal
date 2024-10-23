from django.urls import path
from .views import *

app_name = 'apps.comentario'

urlpatterns = [
    path('comentar/<int:id>/', ComentarPostView.as_view(), name='comentar_post'),
    path('listado_comentario/', ListadoComentarioView.as_view(), name='listado_comentario'),
    path('agregar_comentario/', AgregarComentarioView.as_view(), name='agregar_comentario'),
    path('eliminar_comentario/<int:pk>/', DeleteComentario.as_view(), name='comentario_confirm_delete'),
    path('detalle_post/<int:post_id>/', DetallePostView.as_view(), name='detalle_post'),
]