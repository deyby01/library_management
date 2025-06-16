from urllib import response
from django.test import TestCase
from .models import Autor, Libro, Comentario
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        

    def test_usuario_autenticado_puede_publicar_comentario(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        autor = Autor.objects.create(
            nombre='Arthur',
            apellido='Clarke',
            mini_biografia='Un prolífico escritor de ciencia ficción.'
        )
        libro = Libro.objects.create(
            titulo='Diario de Ana Frank',
            slug='diario-de-ana-frank',
            autor=autor,
            genero='No ficción',
            ISBN='978-0-553-57340-4',
            fecha_publicacion='1947-06-25'
        )
        self.client.login(username='testuser', password='testpassword')
        
        # Simular el envío de un comentario
        datos_del_comentario = {
            'contenido': 'Un libro muy conmovedor.',
        }
        
        # Obtenemos la URL de la pagina de detalle del libro que creamos
        url_del_libro = reverse('catalogo:libro_detalle', kwargs={'slug': libro.slug})
        
        # Enviamos la peticion POST a esa URL con los datos del comentario
        response = self.client.post(url_del_libro, data=datos_del_comentario)
        
        # Verificar
        # Comprobamos que existe un comentario en la base de datos
        self.assertEqual(Comentario.objects.count(), 1)
        
        # Obtenemos ese primer y unico comentario para inspeccionarlo
        primer_comentario = Comentario.objects.first()
        
        # Verificamos que todo se guardo correctamente
        self.assertEqual(primer_comentario.contenido, 'Un libro muy conmovedor.')
        self.assertEqual(primer_comentario.usuario, user)
        self.assertEqual(primer_comentario.libro, libro)


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
        

# Creamos una prueba para ver si podemos acceder a la informacion de un Autor
class AutorListViewTest(TestCase):
    """Pruebas para ver los autores."""
    #1.- Arrangre, preparamos los datos necesarios
    def setUp(self):
        self.autor1 = Autor.objects.create(
            nombre='J.K.',
            apellido='Rowling',
            mini_biografia='Autora de la saga Harry Potter.'
        )
        self.autor2 = Autor.objects.create(
            nombre='J.R.R.',
            apellido='Tolkien',
            mini_biografia='Autor de El Señor de los Anillos.'
        )
        self.autor3 = Autor.objects.create(
            nombre='Isaac',
            apellido='Asimov',
            mini_biografia='Creador de la Fundación y las leyes de la robótica.'
        )
    #2.- Act, solicitamos la url que queremos probar
    def test_pagina_lista_autores_funciona(self):
        response = self.client.get(reverse('catalogo:lista_autores'))
        
        #3.- Assert, verificamos que la respuesta sea correcta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo/lista_autores.html')
        self.assertContains(response, 'Isaac Asimov')


class AutorDetailViewTest(TestCase):
    """Pruebas para ver los detalles de un autor."""
    def setUp(self):
        self.autor = Autor.objects.create(
            nombre='Ray',
            apellido='Bradbury',
            mini_biografia='Autor de Fahrenheit 451.'
        )
        self.libro = Libro.objects.create(
            titulo='Fahrenheit 451',
            slug='fahrenheit-451',
            autor=self.autor,
            genero='Ciencia ficción',
            ISBN='978-0-7432-4722-1',
            fecha_publicacion='1953-10-19'
        )
        self.libro2 = Libro.objects.create(
            titulo='Crónicas Marcianas',
            slug='cronicas-marcianas',
            autor=self.autor,
            genero='Ciencia ficción',
            ISBN='978-0-7432-4723-8',
            fecha_publicacion='1950-09-30'
        )
        self.libro3 = Libro.objects.create(
            titulo='El hombre ilustrado',
            slug='el-hombre-ilustrado',
            autor=self.autor,
            genero='Ciencia ficción',
            ISBN='978-0-7432-4724-5',
            fecha_publicacion='1951-03-01'
        )
        
    def test_autor_detalle_funciona(self):
        url = reverse('catalogo:detalle_autor', kwargs={'pk': self.autor.pk})
        response = self.client.get(url)
        
        # Verificar
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo/detalle_autor.html')
        self.assertContains(response, 'Ray Bradbury')
        self.assertContains(response, 'Fahrenheit 451')
        
        
class RegistroViewTest(TestCase):
    """Pruebas para la vista de registro de usuario."""
    
    def setUp(self):
        """Preparar la URL que usaremos en todas las pruebas de esta clase."""
        self.url = reverse('registro')# Usaremos un nuevo nombre de URL 'registro'
        
    def test_paginas_de_registro_funciona_correctamente(self):
        """Verifica que la pagina de registro carga y usa la plantilla correcta."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registro.html')
        # Verifica que el formulario que se usa es el correcto
        self.assertTrue(isinstance(response.context['form'], UserCreationForm))
        
    def test_registro_crea_nuevo_usuario(self):
        """Verifica que una petición POST crea un nuevo usuario y redirige."""
        # Contamos cuantos usuarios hay al principio (debería ser 0)
        num_usuarios_antes = User.objects.count()
        
        # Preparamos los datos que enviaremos en el formulario
        datos_formulario = {
            'username': 'usuarioprueba',
            'password1': 'contraseña123',
            'password2': 'contraseña123',
        }
        
        # Hacemos la Peticion POST simulando el envío del formulario
        # follow=True le dice al cliente de pruebas que siga la redirección
        response = self.client.post(self.url, data=datos_formulario, follow=True)
        
        
        # Verificamos que se ha creado un nuevo usuario
        self.assertEqual(User.objects.count(), num_usuarios_antes + 1)
        # Verificamos que el usuario nuevo tiene el nombre de usuario correcto
        self.assertEqual(User.objects.first().username, 'usuarioprueba')
        # Verificamos que tras el registro, se redirige a la página de inicio
        self.assertRedirects(response, reverse('login'))


class ComentarioModelTest(TestCase):
    """Pruebas para el modelo comentario."""
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.autor = Autor.objects.create(
            nombre='Isaac',
            apellido='Asimov',
            mini_biografia='Autor de ciencia ficción.'
        )
        self.libro = Libro.objects.create(
            titulo='Fundación',
            slug='fundacion',
            autor=self.autor,
            genero='Ciencia ficción',
            ISBN='978-0-553-80371-0',
            fecha_publicacion='1951-06-01'
        )
        
    def test_se_puede_crear_comentario(self):
        comentario = Comentario.objects.create(
            libro=self.libro,
            usuario=self.user,
            contenido='Un libro fascinante.'
        )
        self.assertEqual(comentario.libro, self.libro)
        self.assertEqual(comentario.usuario, self.user)
        self.assertEqual(comentario.contenido, 'Un libro fascinante.')