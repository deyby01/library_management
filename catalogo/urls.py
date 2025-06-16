from django.urls import path
from .views import PaginaInicioView, LibroDetailView

# Le damos el namespace
app_name = 'catalogo'

urlpatterns = [
    path('', PaginaInicioView.as_view(), name='pagina_inicio'),
    path('libro/<slug:slug>/', LibroDetailView.as_view(), name='libro_detalle'),
]