from django.db import models
from django.conf import settings

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    mini_biografia = models.TextField()

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    genero = models.CharField(max_length=50)
    ISBN = models.CharField(max_length=100, unique=True)
    fecha_publicacion = models.DateField()

    def __str__(self):
        return self.titulo
    
class Comentario(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return self.texto[:50]  # Mostrar los primeros 50 caracteres del comentario