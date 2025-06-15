from django.contrib import admin
from .models import Autor, Libro

# Register your models here.
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido')
    search_fields = ('nombre', 'apellido')

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'genero', 'ISBN', 'fecha_publicacion')
    search_fields = ('titulo', 'autor__nombre', 'autor__apellido', 'genero', 'ISBN')
    ordering = ('fecha_publicacion', 'titulo')
    # Vamos a hacer que el slug se autocomplete al escribir el título
    prepopulated_fields = {'slug': ('titulo',)}