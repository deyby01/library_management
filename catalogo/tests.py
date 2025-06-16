from django.test import TestCase
from .models import Autor, Libro
from django.urls import reverse

class AutorModelTest(TestCase):
    """Pruebas para el modelo Autor."""
    def test_se_puede_crear_un_autor(self):
        autor = Autor.objects.create(
            nombre='Stephen',
            apellido='King',
            mini_biografia='Un prolífico escritor de terror.'
        )
        self.assertEqual(autor.nombre, 'Stephen')
        self.assertEqual(autor.apellido, 'King')
        

class LibroModelTest(TestCase):
    """Pruebas para el modelo Libro."""
    def test_se_puede_crear_libro_con_autor(self):
        autor_prueba = Autor.objects.create(nombre='Ursula K.', apellido='Le Guin', mini_biografia='Autora de ciencia ficción.')
        libro = Libro.objects.create(
            titulo='Un Mago de Terramar',
            slug='un-mago-de-terramar',
            autor=autor_prueba,
            genero='Fantasía',
            ISBN='978-0-06-025492-6',
            fecha_publicacion='2007-08-27'
        )
        self.assertEqual(libro.titulo, 'Un Mago de Terramar')
        self.assertEqual(libro.autor, autor_prueba)
        self.assertEqual(libro.genero, 'Fantasía')
        self.assertEqual(libro.ISBN, '978-0-06-025492-6')
        self.assertEqual(libro.fecha_publicacion, '2007-08-27')
        
    def test_vista_detalle_libro(self):
        autor = Autor.objects.create(
            nombre='George',
            apellido='Orwell',
            mini_biografia='Escritor británico, conocido por sus obras distópicas.'
        )
        libro = Libro.objects.create(
            titulo='El gran hermano',
            slug='el-gran-hermano',
            autor=autor,
            genero='Distopía',
            ISBN='978-0-452-28423-4',
            fecha_publicacion='1949-06-08'
        )
        
        url = reverse('catalogo:libro_detalle', kwargs={'slug': libro.slug})
        response = self.client.get(url)
        
        # Verificar
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'El gran hermano')
        self.assertContains(response, 'George Orwell')
        self.assertTemplateUsed(response, 'catalogo/libro_detalle.html')
        


class PaginaInicioViewTest(TestCase):
    """Pruebas para la vista de la página de inicio."""
    def setUp(self):
        self.autor = Autor.objects.create(
            nombre='Gabriel',
            apellido='García Márquez',
            mini_biografia='Escritor colombiano, ganador del Premio Nobel.'
        )
        self.libro = Libro.objects.create(
            titulo='Cien años de soledad',
            slug='cien-anos-de-soledad',
            autor=self.autor,
            genero='Realismo mágico',
            ISBN='978-3-16-148410-0',
            fecha_publicacion='1967-06-05'
        )
        self.libro2 = Libro.objects.create(
            titulo='El otoño del patriarca',
            slug='el-otono-del-patriarca',
            autor=self.autor,
            genero='Realismo mágico',
            ISBN='978-3-16-148410-1',
            fecha_publicacion='1975-02-01'
        )
        self.libro3 = Libro.objects.create(
            titulo='Crónica de una muerte anunciada',
            slug='cronica-de-una-muerte-anunciada',
            autor=self.autor,
            genero='Realismo mágico',
            ISBN='978-3-16-148410-2',
            fecha_publicacion='1981-04-06'
        )
        
    def test_pagina_inicio_muestra_libros(self):
        response = self.client.get(reverse('catalogo:pagina_inicio'))
        
        # Verificar
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo/inicio.html')
        self.assertContains(response, 'Cien años de soledad')
        self.assertContains(response, 'Crónica de una muerte anunciada')    
        
