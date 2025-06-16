from django.shortcuts import render
from .models import Libro, Autor
from django.views.generic import ListView, DetailView

# Create your views here.


class PaginaInicioView(ListView):
    """Vista para la página de inicio que muestra una lista de libros de la base de datos."""
    model = Libro
    template_name = 'catalogo/inicio.html'
    context_object_name = 'libros'
    
class LibroDetailView(DetailView):
    """Vista para mostrar los detalles de un libro específico."""
    model = Libro
    template_name = 'catalogo/libro_detalle.html'
    context_object_name = 'info_libro'
    
class AutorListView(ListView):
    """Vista para mostrar una lista de autores."""
    model = Autor
    template_name = 'catalogo/lista_autores.html'
    context_object_name = 'autores'
    
class AutorDetailView(DetailView):
    """Vista para mostrar los detalles de un autor especifico."""
    model = Autor
    template_name = 'catalogo/detalle_autor.html'
    context_object_name = 'info_autor'