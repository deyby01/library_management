# en catalogo/tests.py

from django.test import TestCase
from .models import Autor, Libro

class AutorModelTest(TestCase):
    def test_se_puede_crear_un_autor(self):
        autor = Autor.objects.create(
            nombre='Stephen',
            apellido='King',
            mini_biografia='Un prolífico escritor de terror.'
        )
        self.assertEqual(autor.nombre, 'Stephen')
        self.assertEqual(autor.apellido, 'King')
        

class LibroModelTest(TestCase):
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