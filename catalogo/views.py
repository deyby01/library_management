from django.shortcuts import render
from .models import Libro, Autor
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .forms import ComentarioForm
from django.shortcuts import redirect

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
    
    #1. pasamos el formulario al contexto para poder mostrarlo en la plantilla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        context['comentarios'] = self.get_object().comentarios.all()  # Obtenemos los comentarios del libro actual
        return context
    
    # 2. Manejamos la peticion POST que envia el formulario
    def post(self, request, *args, **kwargs):
        form = ComentarioForm(request.POST)
        if form.is_valid():
            # Creamos el objeto Comentario pero aun no lo guardamos en la base de datos
            comentario = form.save(commit=False)
            
            # Asignamos el libro y el usuario al comentario (que no venian en el formulario)
            comentario.libro = self.get_object()  # Obtenemos el libro actual
            comentario.usuario = request.user
            
            # Ahora si guardamos el comentario completo
            comentario.save()
            
            # Redirigimos a la misma pagina para ver el comentario nuevo
            return redirect(request.path_info)  # Redirige a la misma URL   
        
        # Si el formulario no es valido, lo volvemos a mostrar con los errores
        return super().get(request, *args, **kwargs)
    
    
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