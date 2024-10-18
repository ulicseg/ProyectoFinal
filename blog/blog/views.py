from django.shortcuts import render
from django.http import HttpResponseNotFound

def index(request):
    return render(request, 'index.html')

def pagina_404(request, exception):
    return HttpResponseNotFound('<h1>La pagina no existe</h1>')

