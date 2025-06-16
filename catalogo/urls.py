from django.urls import path
from .views import PaginaInicioView, LibroDetailView, AutorListView, AutorDetailView

# Le damos el namespace
app_name = 'catalogo'

urlpatterns = [
    path('', PaginaInicioView.as_view(), name='pagina_inicio'),
    path('libro/<slug:slug>/', LibroDetailView.as_view(), name='libro_detalle'),
    path('autores/', AutorListView.as_view(), name='lista_autores'),
    path('autor/<int:pk>/', AutorDetailView.as_view(), name='detalle_autor'),
]