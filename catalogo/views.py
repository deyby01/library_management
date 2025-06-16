from django.shortcuts import render
from .models import Libro
from django.views.generic import ListView, DetailView

# Create your views here.
class PaginaInicioView(ListView):
    model = Libro
    template_name = 'catalogo/inicio.html'
    context_object_name = 'libros'
    
class LibroDetailView(DetailView):
    model = Libro
    template_name = 'catalogo/libro_detalle.html'
    context_object_name = 'info_libro'