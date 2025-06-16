from django.shortcuts import render
from .models import Libro, Autor
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

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
    
class RegistroView(CreateView):
    """Vista para el registro de nuevos usuarios."""
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registro.html'